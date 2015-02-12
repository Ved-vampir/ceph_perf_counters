#!/usr/local/bin/python

import sys
import argparse
import json
import texttable as TT
import perfcollect as PC


# function to read config file
def get_perfcounters_list_from_config(config):
    clist = open(config).read()
    return json.loads(clist)


# function to get counters list from args
def get_perfcounters_list_from_sysargs(args):
    pc = dict()
    for lst in args:
        pc[lst[0]] = []
        for i in range(1, len(lst)):
            pc[lst[0]].append(lst[i])
    return pc


# function for table output of counters values
def output_to_table(perf_counters, perf_list):
    # prepare data for table output
    tab = TT.Texttable()
    tab.set_deco(tab.HEADER | tab.VLINES | tab.BORDER | tab.HLINES)

    header = ['']
    header.extend(perf_list.keys())
    tab.add_row(header)
    tab.header = header

    for group_name, counters in perf_counters.items():
        row = [''] * (len(perf_list.keys()) + 1)
        row[0] = group_name
        tab.add_row(row)
        for counter in counters:
                row = []
                row.append(counter)
                for key, value in perf_list.items():
                    if (group_name in value and counter in value[group_name]):
                        if type(value[group_name][counter]) != type(dict()):
                            row.append(value[group_name][counter])
                        else:
                            s = ""
                            for key1, value1 in value[group_name][counter].items():
                                s = s + key1 + " = " + str(value1) + "\n"
                            row.append(s)
                tab.add_row(row)

    print (tab.draw())


# save counters in json file
def output_to_json (perf_counters, perf_list, filename):
    # select info
    save = dict()
    for node, value in perf_list.items():
        save[node] = dict()
        for group_name, counters in perf_counters.items():
            if (group_name in value):
                save[node][group_name] = dict()
                for counter in counters:
                    if (counter in value[group_name]):
                        save[node][group_name][counter] = value[group_name][counter]
    # save info
    with open(filename, 'w') as f:
        json.dump(save, f, indent=4)


def main():
    # parse command line
    ag = argparse.ArgumentParser(description="Collect perf counters from ceph nodes", 
                                    epilog="Note, if you don't use both -c and -g options, all counters will be collected.")
    ag.add_argument("--ip", "-i", type=str, help="Controller host")
    ag.add_argument("--user", "-u", type=str, help="User name for all hosts")
    ag.add_argument("--json", "-j", type=str, help="Output to file in json format, you need specify file name")
    ag.add_argument("--config", "-g", type=str, 
                        help="Use it, if you want upload needed counter names from file (json format, .counterslist as example)")
    ag.add_argument("--collection", "-c", type=str, action="append", nargs='+', 
                        help="Counter collections in format collection_name counter1 counter2 ...")
    args = ag.parse_args()

    # check some errors in command line
    if (args.collection is not None):
        for lst in args.collection:
            if (len(lst) < 2):
                print ("Collection argument must contain at least one counter")
                return 1
    if (args.config is not None and args.collection is not None):
        print ("You cannot add counters from config and command line together")
        return 1
    if (args.ip is None):
        print ("Warning: you try to connect to default host (local)!\n")

    # prepare info about needed counters
    if (args.config is not None):
        perf_counters = get_perfcounters_list_from_config(args.config)
    elif (args.collection is not None):
        perf_counters = get_perfcounters_list_from_sysargs(args.collection)
    else:
        perf_counters = None

    # send parameters to external function
    params = {}
    if (args.ip is not None):
        params["host"] = args.ip
    if (args.user is not None):
        params["user"] = args.user
    if (perf_counters is None):
        params["wantschema"] = True
        params["withouttype"] = True

    perf_list = PC.get_perf_dump_in_map(**params)

    # if all counters required, schema is in result too
    if (perf_counters is None):
        perf_counters = perf_list[0]
        perf_list = perf_list[1]

    if (args.json is None):
        output_to_table(perf_counters, perf_list)
    else:
        output_to_json(perf_counters, perf_list, args.json)


if __name__ == '__main__':
    main()
