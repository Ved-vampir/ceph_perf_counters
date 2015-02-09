#!/usr/local/bin/python

import sys
import argparse
import json
import texttable as TT
import perfcollect as PC

# set here counters, which you need, in format group - list of counters
perf_counters = {'WBThrottle': ['bytes_dirtied', 'ios_dirtied'],
                 'filestore': ['journal_latency', 'journal_queue_max_ops', 'commitcycle_interval']}


def get_perfcounters_list_from_config(config):
# function to read config file
    clist = open(config).read()
    return json.loads(clist)

def get_perfcounters_list_from_sysargs(args):
# function to get counters list from args
    pc = dict()
    for lst in args:
        pc[lst[0]] = []
        for i in range(1,len(lst)):
            pc[lst[0]].append(lst[i])
    return pc


def main(): 
    # parse command line
    ag = argparse.ArgumentParser(description="Collect perf counters from ceph nodes",
                                    epilog="Note, if you don't use both -c and -g options, counter names from the code will be used.")
    ag.add_argument("--ip","-i",type=str,help="Controller host")
    ag.add_argument("--user","-u",type=str,help="User name for all hosts")
    ag.add_argument("--config","-g",type=str,help="Use it, if you want upload needed counter names from file (json format, .counterslist as example)")
    ag.add_argument("--collection","-c",type=str,action="append",nargs='+',help="Counter collections in format collection_name counter1 counter2 ...")
    args = ag.parse_args()

    # check some errors in command line
    if (args.collection != None):
        for lst in args.collection:
            if (len(lst) < 2):
                print ("Collection argument must contain at least one counter")
                return 1
    if (args.config != None and args.collection != None):
        print ("You cannot add counters from config and command line together")
        return 1

    # prepare info about needed counters
    if (args.config != None):
        perf_counters = get_perfcounters_list_from_config (args.config)
    if (args.collection != None):
        perf_counters = get_perfcounters_list_from_sysargs (args.collection)

    # send parameters to external function
    if (args.ip == None and args.user == None):
        perf_list = PC.get_perf_dump_in_map()
    elif (args.ip != None and args.user == None):
        perf_list = PC.get_perf_dump_in_map(host=args.ip)
    elif (args.ip == None and args.user != None):
        perf_list = PC.get_perf_dump_in_map(user=args.user)
    else:
        perf_list = PC.get_perf_dump_in_map(host=args.ip,user=args.user)

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
                if type(value[group_name][counter]) != type(dict()):
                    row.append(value[group_name][counter])
                else:
                    s = ""
                    for key1, value1 in value[group_name][counter].items():
                        s = s + key1 + " = " + str(value1) + "\n"
                    row.append(s)
            tab.add_row(row)


    print (tab.draw())


if __name__ == '__main__':
    main()
