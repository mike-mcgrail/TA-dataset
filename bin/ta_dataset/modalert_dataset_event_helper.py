import requests
import json
import datetime
import uuid

# encoding = utf-8
#set DataSet API url based on environment
def set_url(helper):
    if helper.get_global_setting('dataset_eu_environment') == True:
        return 'https://app.eu.scalyr.com/api/addEvents'
    else:
        return 'https://app.scalyr.com/api/addEvents'


def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example gets the setup parameters and prints them to the log
    dataset_eu_environment = helper.get_global_setting("dataset_eu_environment")
    helper.log_info("dataset_eu_environment={}".format(dataset_eu_environment))
    dataset_log_read_access_key = helper.get_global_setting("dataset_log_read_access_key")
    helper.log_info("dataset_log_read_access_key={}".format(dataset_log_read_access_key))
    dataset_log_write_access_key = helper.get_global_setting("dataset_log_write_access_key")
    helper.log_info("dataset_log_write_access_key={}".format(dataset_log_write_access_key))

    # The following example gets the alert action parameters and prints them to the log
    dataset_serverhost = helper.get_param("dataset_serverhost")
    helper.log_info("dataset_serverhost={}".format(dataset_serverhost))

    dataset_message = helper.get_param("dataset_message")
    helper.log_info("dataset_message={}".format(dataset_message))

    dataset_severity = helper.get_param("dataset_severity")
    helper.log_info("dataset_severity={}".format(dataset_severity))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    
    helper.set_log_level(helper.log_level)
    helper.log_debug("Alert action dataset_event started.")

    # TODO: Implement your alert action logic here
    ds_uuid = str(uuid.uuid4())
    ds_url = set_url(helper)
    ds_api_key = helper.get_global_setting('dataset_log_write_access_key')
    ds_headers = { "Authorization": "Bearer " + ds_api_key }
    dataset_serverhost = helper.get_param('dataset_serverhost')
    dataset_severity = int(helper.get_param('dataset_severity'))
    dataset_message = helper.get_param('dataset_message')
    
    events = helper.get_events()
    counter = 1
    
    for event in events:

        #convert ISO 8601 to epoch nanoseconds
        epoch_time = datetime.datetime.strptime(event['_time'],
                             "%Y-%m-%dT%H:%M:%S.%f%z")
        ds_time = epoch_time.timestamp() * 1000000000
        ds_timestamp = str("%.0f" % ds_time)
        
        #format payload for DataSet addEvents API
        ds_event_dict = {
            "session": ds_uuid,
            "sessionInfo": {
                "serverHost": dataset_serverhost
            },
            "events": [
                {
                    "thread": str(counter),
                    "ts": ds_timestamp,
                    "sev": dataset_severity,
                    "tag": "splunk",
                    "attrs": {
                        "message": dataset_message,
                        "Application": "splunk"
                    }
                }
            ],
            "threads": [
                {
                    "id": counter,
                    "name": "splunk alert " + str(counter)
                }
            ]
        }
        
        ds_payload = json.loads(json.dumps(ds_event_dict))
        counter +=1
        
        try:
            r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
            
            helper.log_debug("response = %s" % r.text)
            
        except Exception as e:
            helper.log_error(e)