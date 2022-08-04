# encoding = utf-8

import os
import sys
import time
import datetime
import json
import requests
from urllib.parse import urljoin, urlencode
import ast
import ta_dataset_declare

# Enterprise SDK imports
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators


# 'https://app.scalyr.com/api/query?queryType=log&maxCount=1&token=XXX'
def set_url(eu_bool):
    if eu_bool == True:
        return 'https://app.eu.scalyr.com/api/'
    else:
        return 'https://app.scalyr.com/api/'


def get_token(self):
    #use Python SDK secrets retrieval
    for credential in self.service.storage_passwords:
        cred = credential.content.get('clear_password')

        #add-on builder uses custom names, so instead of by name filter resulting string to known key
        if 'dataset_log_read_access_key' in cred:
            #convert string to json and get corresponding value
            cred_json = json.loads(cred)
            token = cred_json['dataset_log_read_access_key']
            return token


@Configuration()
class DataSetSearch(GeneratingCommand):
    query = Option(doc='''
        **Syntax: query=<string>
        **Description:** the DataSet query used to filter events. Default is no filter (return all events limited by maxCount).''', 
        require=False)

    startTime = Option(doc='''
        **Syntax: startTime=<string>
        **Description:** the start time for events to return from DataSet. Default is 1 minute (1m).''', 
        require=False, validate=validators.Match('time', '\d+(d|h|m|s)'))

    endTime = Option(doc='''
        **Syntax: endTime=<string>
        **Description:** the end time for events to return from DataSet. Default is current time.''', 
        require=False, validate=validators.Match('time', '\d+(d|h|m|s)'))

    maxCount = Option(doc='''
        **Syntax: maxCount=<integer>
        **Description:** the number of events to return from DataSet. Default is 100.''', 
        require=False, default=100, validate=validators.Integer())

    def generate(self):

        conf = self.service.confs['ta_dataset_settings']['additional_parameters'].content
        #convert single quote key: value to proper json "key": "value"
        conf_j = json.dumps(conf)
        conf_json = json.loads(conf_j)
        environment = int(conf_json['dataset_eu_environment'])

        #set DataSet url and get API key
        ds_url = set_url(environment)
        ds_api_key = get_token(self)

        #error if no api key provided in settings
        if not ds_api_key:
            yield { '_raw': 'read api key error, check add-on settings' }
            exit(0)

        #set default values for query
        ds_url += 'query'
        ds_headers = { "Authorization": "Bearer " + ds_api_key }
        ds_payload = { "queryType": "log", "startTime": '1m' }

        ##### Parse user-provided options
        if self.query:
            ds_payload['filter'] = self.query
        
        if self.startTime:
            ds_payload['startTime'] = self.startTime
        
        if self.endTime:
            ds_payload['endTime'] = self.endTime

        if self.maxCount:
            ds_payload['maxCount'] = self.maxCount
        
        try:
            #make request
            r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
            r_json = r.json()

            matches = r_json['matches']
            sessions = r_json['sessions']
            
            for match_list in matches:
                ds_event_dict = {}
                ds_event_dict = match_list
                session_key = match_list['session']

                for session_entry, session_dict in sessions.items():
                    if session_entry == session_key:
                        for key in session_dict:
                            ds_event_dict[key] = session_dict[key]

                ds_event = json.loads(json.dumps(ds_event_dict))
                #convert epoch nanoseconds to seconds for Splunk
                ds_dt = int(ds_event['timestamp'])
                splunk_dt = ds_dt / 1000000000

                yield {
                    '_raw': ds_event,
                    '_time': splunk_dt,
                    'source': 'dataset_command',
                    'sourcetype': 'dataset:query'
                }
        except:
            yield { '_raw': 'error connecting to DataSet' }

dispatch(DataSetSearch, sys.argv, sys.stdin, sys.stdout, __name__)