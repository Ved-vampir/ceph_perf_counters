#!/usr/local/bin/python

import time
from contextlib import contextmanager
import perfcollect as PC

class CountersTimer(object):

    # perf_counters 
    # perf_values0 perf_values1
    # host
    # user
    # perf_difference

    def __init__(self, perf_counters=None, host="127.0.0.1", user="root"):
        self.perf_counters = perf_counters
        self.host = host
        self.user = user

    def __enter__(self):
        # getting initial counters values
        if (self.perf_counters is not None): 
            self.perf_values0 = PC.get_perf_dump_in_map(host=self.host, user=self.user, nomess=True)
        else: # if there are no info about coounters - ask from host
            res = PC.get_perf_dump_in_map(host=self.host, user=self.user, nomess=True, wantschema=True, withouttype=True)
            self.perf_values0 = res[1]
            self.perf_counters = res[0]

        return self  # this will be return in as by with statement

    def __exit__(self, *args):
        # getting final counters values
        self.perf_values1 = PC.get_perf_dump_in_map(host=self.host, user=self.user, nomess=True)
        # compute counters difference on specified counters (or on all, if nothing was specified)
        self.perf_difference = dict()

        for grname, cname in self.perf_counters.items():
            
            for c in cname:
                counter = grname+"."+c                      #key = <group name>.<counter name>
                self.perf_difference[counter] = dict()

                for node, value in self.perf_values1.items():

                    # test if this counter is in result 
                    if ((grname in self.perf_values0[node]) and (c in self.perf_values0[node][grname])):

                        dif0 = self.perf_values0[node][grname][c]
                        dif1 = value[grname][c]

                        if (type(dif0) != type(dict())):
                            self.perf_difference[counter][node] = dif1-dif0
                        else:  # in a case of complex counter
                            self.perf_difference[counter][node] = dict()
                            for k, v in dif1.items():
                                self.perf_difference[counter][node][k] = v - dif0[k]




def main(): # just for test
    perf_counters = {'WBThrottle': ['bytes_dirtied', 'ios_dirtied'],
                    'filestore': ['journal_latency', 'journal_queue_max_ops']}
    ct = CountersTimer(host="172.16.54.71",perf_counters=perf_counters)
    with ct as result:
        pass#time.sleep(10)
    print ("Res: ", result.perf_difference)


if __name__ == '__main__':
    main()

