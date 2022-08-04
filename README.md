#  TA-dataset
The DataSet Add-on for Splunk provides integration with [DataSet](https://www.dataset.com) by [SentinelOne](https://sentinelone.com). The key functions allow two-way integration:
- inputs to index alerts or user-defined query results from DataSet into Splunk
- SPL custom command to query against DataSet directly from the Splunk UI
- alert action to send an event to DataSet

## Inputs
The DataSet Add-on for Splunk collects the following inputs:

| Source Type | Description | CIM Data Model
| ------ | ------ | ------ |
| dataset:alerts | Predefined Power Query API call to index [alert state change records](https://app.scalyr.com/help/alerts#logging)  | [Alerts](https://docs.splunk.com/Documentation/CIM/latest/User/Alerts)
| dataset:query | User-defined standard [query](https://app.scalyr.com/help/api#query) API call to index events | -

## SPL Custom Command
The `| dataset` command allows queries against the DataSet API directly from Splunk's SPL bar. Four optional parameters are supported:

- **query** - the DataSet [query](https://app.scalyr.com/help/query-language) used to filter events. Default is no filter (return all events limited by maxCount).
- **startTime** - the [start time](https://app.scalyr.com/help/time-reference) for DataSet events to return. Use relative shorthand in the form of a number followed by d, h, m or s (for days, hours, minutes or seconds), e.g.: 24h
- **endTime** - the [end time](https://app.scalyr.com/help/time-reference) for DataSet events to return. Use relative shorthand in the form of a number followed by d, h, m or s (for days, hours, minutes or seconds), e.g.: 5m
- **maxCount** - the number of events to return from DataSet. Default is 100

Example:
`
| dataset query="serverHost = * AND Action = 'allow'" startTime=10m endTime=1m maxCount=50
`

Since events are returned in JSON format, the Splunk [spath command](https://docs.splunk.com/Documentation/SplunkCloud/latest/SearchReference/Spath) is useful:

```
| dataset query="serverHost = * AND Action = 'allow'" startTime=10m endTime=1m maxCount=50
| spath
```

## Alert Action
An alert action allows sending an event to the DataSet [addEvents API](https://app.scalyr.com/help/api#addEvents). 

## Current Version Limitations
- Limit of 5,000 events returned from DataSet
- No proxy support

## Known Issues
- SPL custom command startTime and endTime validator RegEx allows multiple characters (e.g. `1hh` should fail)