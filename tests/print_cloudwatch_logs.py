#!/usr/bin/env python

import common_funcs


log_group_name = '/aws/lambda/lambda-func'


def main():
    client = common_funcs.get_client(service="logs")
    log_streams_resp = client.describe_log_streams(logGroupName=log_group_name)
    log_streams = [log_stream["logStreamName"] for log_stream in log_streams_resp["logStreams"]]

    log_stream_event_msg_all = dict()

    for log_stream_name in log_streams:
        log_stream_events = client.get_log_events(logGroupName=log_group_name, logStreamName=log_stream_name)
        log_stream_event_msg_all[log_stream_name] = [event["message"] for event in log_stream_events["events"]]

    for stream_name, events in log_stream_event_msg_all.items():
        print(f"\n{stream_name}")
        for event in events:
            print(event.encode("utf-8"))
        print("---------------------------")


if __name__ == "__main__":
    main()

