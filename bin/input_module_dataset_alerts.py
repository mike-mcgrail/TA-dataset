# encoding = utf-8

import os
import sys
import time
import datetime
import json
import requests

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
    pass


#set DataSet API url based on environment
def set_url(helper):
    if helper.get_global_setting('dataset_eu_environment') == True:
        return 'https://app.eu.scalyr.com/api/powerQuery'
    else:
        return 'https://app.scalyr.com/api/powerQuery'


#set DataSet query
def set_ds_query(ds_start_time):
    ds_query = { "query": "tag=\'alertStateChange\' status=2 | columns timestamp, app, silencedUntilMs, gracePeriod, lastRedAlertMs, reportedStatus, renotifyPeriod, lastTriggeredNotificationMinutes, description, severity, trigger, lastStatus, status", "startTime": ds_start_time }
    return ds_query


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
    # In single instance mode, to get arguments of a particular input, use
    opt_start_time = helper.get_arg('start_time', stanza_name)

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
    global_dataset_log_read_access_key = helper.get_global_setting("dataset_log_read_access_key")
    global_dataset_eu_environment = helper.get_global_setting("dataset_eu_environment")

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
    #use DataSet PowerQuery to limit returned fields
    ds_payload = set_ds_query(ds_start_time)
    
    '''
    example of PowerQuery results:
    {
    "columns": [
        {
            "name": "timestamp"
        },
        {
            "name": "app"
        },
        {
            "name": "silencedUntilMs"
        },
        {
            "name": "gracePeriod"
        },
        {
            "name": "lastRedAlertMs"
        },
        {
            "name": "reportedStatus"
        },
        {
            "name": "renotifyPeriod"
        },
        {
            "name": "lastTriggeredNotificationMinutes"
        },
        {
            "name": "description"
        },
        {
            "name": "severity"
        },
        {
            "name": "trigger"
        },
        {
            "name": "lastStatus"
        },
        {
            "name": "status"
        }
    ],
    "warnings": [
        "Result set limited to 1000 rows by default. To display more rows, add a command like \"| limit 10000\"."
    ],
    "values": [
        [
            1658762001620795544,
            "appserver",
            0,
            0,
            1658760799604,
            1,
            60,
            20,
            "Delays over 7.5s",
            3,
            "count:2 minutes(timeMs > 7500) > 2",
            1,
            2
        ],
        [
            1658767160258414975,
            "cloudWatchLogs",
            0,
            0,
            1658766860380,
            1,
            0,
            4,
            "Errors on cloudWatchLogs",
            3,
            "count:2 minutes((\"error\") ($serverHost contains \"cloudWatchLogs\"))/count:2 minutes(!(\"error\") ($serverHost contains \"cloudWatchLogs\")) > 0",
            1,
            2
        ],
        ...<more value lists>...
        "matchingEvents": 9.0,
        "status": "success",
        "omittedEvents": 0.0
    '''
    
    try:
        r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
        r_json = r.json() #parse results json
        
        #log information from results
        if r_json['status']:
            helper.log_info("response status=%s" % str(r_json['status']))
         
        if r_json['warnings']:
            for warning in r_json['warnings']:
                helper.log_info("response warning=%s" % str(warning))
            
        if r_json['matchingEvents']:
            helper.log_info("response matches=%s" % str(r_json['matchingEvents']))
            
        if r_json['omittedEvents']:
            helper.log_warning("response omitted=%s" % str(r_json['omittedEvents']))
        
        #parse results, match returned columns with corresponding values
        ds_event_dict = {}
        for value_list in r_json['values']:
            for counter in range(len(value_list)):
                ds_event_dict[r_json['columns'][counter]['name']] = value_list[counter]
        
            #check event time against checkpoint
            #PowerQuery results are returned by default in chronological order
            checkpoint_key = helper.get_input_type() + "_key"
            event_time = ds_event_dict['timestamp']
            validated_checkpoint = compare_checkpoint(helper, checkpoint_key, event_time)
        
            #if greater than current checkpoint, update checkpoint and write event
            if validated_checkpoint:
                helper.log_info("saving checkpoint %s" % (str(event_time)))
                helper.save_check_point(checkpoint_key, event_time)
                ds_event = json.dumps(ds_event_dict)
                write_events(helper, ew, str(ds_event))
                
    except Exception as e:
        helper.log_error(e)


def write_events(helper, ew, data):
    helper.log_debug("writing event %s" % data)
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
