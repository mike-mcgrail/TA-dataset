# encoding = utf-8

import os
import sys
import time
import datetime
import json
import requests
from collections import OrderedDict
'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # start_time = definition.parameters.get('start_time', None)
    # end_time = definition.parameters.get('end_time', None)
    # dataset_querystring = definition.parameters.get('dataset_query_string', None)
    # max_count = definition.parameters.get('max_count', None)
    pass


#set DataSet API url based on environment
def set_url(helper):
    if helper.get_global_setting('dataset_eu_environment') == True:
        return 'https://app.eu.scalyr.com/api/query'
    else:
        return 'https://app.scalyr.com/api/query'


#get checkpoint, set initial value to 0 if nonexistent
def get_checkpoint(helper, key):
    state = helper.get_check_point(key)

    #if state exists, return it
    if (state not in [None,'']):
        return state
    #if nonexistent, set to 0 for 1st iteration
    else:
        helper.log_info("checkpoint is 0")
        return 0


#compare timestamp to checkpoint value
def compare_checkpoint(helper, key, data):
    checkpoint_time = get_checkpoint(helper, key)
    event_time = data

    if checkpoint_time == 0 or (event_time > checkpoint_time):
        return True
    else:
        helper.log_info("skipping due to event_time=%s is less than checkpoint=%s" % (str(event_time), str(checkpoint_time)))
        return False
        

def collect_events(helper, ew):
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_start_time = helper.get_arg('start_time')
    opt_end_time = helper.get_arg('end_time')
    opt_dataset_query_string = helper.get_arg('dataset_query_string')
    opt_max_count = helper.get_arg('max_count')
    # In single instance mode, to get arguments of a particular input, use
    opt_start_time = helper.get_arg('start_time', stanza_name)
    opt_end_time = helper.get_arg('end_time', stanza_name)
    opt_dataset_query_string = helper.get_arg('dataset_query_string', stanza_name)
    opt_max_count = helper.get_arg('max_count', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_dataset_eu_environment = helper.get_global_setting("dataset_eu_environment")
    global_dataset_log_read_access_key = helper.get_global_setting("dataset_log_read_access_key")
    global_dataset_log_write_access_key = helper.get_global_setting("dataset_log_write_access_key")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
    ds_url = set_url(helper)
    ds_api_key = helper.get_global_setting('dataset_log_read_access_key')
    ds_headers = { "Authorization": "Bearer " + ds_api_key }
    ds_start_time = helper.get_arg('start_time')
    ds_end_time = helper.get_arg('end_time')
    ds_query = helper.get_arg('dataset_query_string')
    #ds_query = ds_query.replace("'", "\\'")
    ds_max_count = helper.get_arg('max_count')

    ds_payload = { "queryType": "log", "startTime": ds_start_time }
    if ds_end_time:
        ds_payload['endTime'] = ds_end_time
    if ds_query:
        ds_payload['filter'] = ds_query
    if ds_max_count:
        ds_payload['maxCount'] = ds_max_count
    
    #write_events(helper, ew, str(json.dumps(ds_payload)))
    try:

        r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
        r_json = r.json() #parse results json
        
        #log information from results
        if r_json['status']:
            helper.log_info("response status=%s" % str(r_json['status']))
            
        #response includes good information for debug logging
        if r_json['status'] == 'success':
            if r_json['executionTime']:
                helper.log_debug("executionTime %s" % (str(r_json['executionTime'])))
            if r_json['cpuUsage']:
                helper.log_debug("cpuUsage is %s" % (str(r_json['cpuUsage'])))
        
        #if successful and results, parse the response
        if r_json['status'] == 'success' and len(r_json['matches']) > 0:
            
            #parse results, match returned matches with corresponding sessions
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

                ordered_ds_event_dict = OrderedDict(ds_event_dict)
                #move timestamp to beginning for efficient Splunk timestamp parsing
                ordered_ds_event_dict.move_to_end('timestamp', last=False)
        
                #check event time against checkpoint
                #PowerQuery results are returned by default in chronological order
                checkpoint_key = helper.get_input_type() + "_key"
                event_time = int(ordered_ds_event_dict['timestamp'])
                validated_checkpoint = compare_checkpoint(helper, checkpoint_key, event_time)
        
                #if greater than current checkpoint, update checkpoint and write event
                if validated_checkpoint:
                    helper.log_info("saving checkpoint %s" % (str(event_time)))
                    helper.save_check_point(checkpoint_key, event_time)
                    ds_event = json.dumps(ordered_ds_event_dict)
                    write_events(helper, ew, str(ds_event))
                
    except Exception as e:
        write_events(helper, ew, str(e))
        helper.log_error(e)


def write_events(helper, ew, data):
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)