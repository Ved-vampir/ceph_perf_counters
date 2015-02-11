# Ceph Perf counters collection tool
Script to collect internal [ceph performance counters](http://ceph.com/docs/master/dev/perf_counters/) from all osds and get some of them.

##Preusage notes
###Build
Some external libraries are used:
 * fabric
 * texttable

###Prepare access
You need to have ssh access for all ceph nodes.  
You can do it manually like this:  
 1. Put your .pub file (with public key) on Fuel node (like this, for example scp .ssh/id_rsa.pub root@\<fuel_node\>:/root/myrsa.pub)  
 2. Next send it from Fuel node by ssh-copy-id on all nodes from 'fuel --env-id \<env_id\> node list' (or only to controller and ceph nodes)  
Or you can use script ./get_access.sh \<fuel_host\> \<environment_name\>. This script uses algorithm, described above. You need to know root password of fuel host and to have local rsa key, named id_rsa. Note, that it is only for convenience, it can be not very safe or have any other problems. Read script for additional information.

I'm sure, there are better ways :)

##Usage

###perfcollect.py

This module contains functions, directly examining nodes. Only one function it make sence to call outside  

	get_perf_dump_in_map(host=cnt_host, user=default_user, nomess=False, wantschema=False, withouttype=False)  

Function returns perf dump for all osds in dict (format like \{"osdname":\{"collection":\{"counter":value,...\})  

Optional parameters:  

    host: controller host, if you don't specify it, localhost will be used
    user: user for login, root by default
    nomess: flag to supress info messages, like "Collecting..."
    wantschema: flag for to query counters schema, if it is True function returns array, schema in dict on \[0\] and perf dump on \[1\]
    withouttype: flag for to clear schema of counter's types (valid only with wantschema = True)

###get_perfs.py

Program, which provides table output for optional counters. Counters can be specified in json file, in command line arguments or all will be used by default.

Usage:

    python get_perfs.py [-h] [--ip IP] [--user USER] [--config CONFIG]
                        [--collection COLLECTION [COLLECTION ...]]

    Tool collects perf counters from ceph nodes and provides it in table format.

    optional arguments:
      -h, --help            show this help message and exit
      --ip IP, -i IP        Controller host
      --user USER, -u USER  User name for all hosts
      --config CONFIG, -g CONFIG
                            Use it, if you want upload needed counter names from
                            file (json format, .counterslist as example)
      --collection COLLECTION [COLLECTION ...], -c COLLECTION [COLLECTION ...]
                            Counter collections in format collection_name counter1
                            counter2 ...

    Note, if you don't use one of -c or -g options, all counters from perf schema will be used.

    You will get output like this:

            Collecting.....
            +-----------------------+-------------------+-------------------+
            |                       | osd0              | osd1              |
            +-----------------------+-------------------+-------------------+
            | filestore             |                   |                   |
            +-----------------------+-------------------+-------------------+
            | journal_latency       | sum = 466.040819  | sum = 540.105306  |
            |                       | avgcount = 32700  | avgcount = 34819  |
            +-----------------------+-------------------+-------------------+
            | journal_queue_max_ops | 0                 | 0                 |
            +-----------------------+-------------------+-------------------+
            | commitcycle_interval  | sum = 4690.277342 | sum = 4648.674446 |
            |                       | avgcount = 922    | avgcount = 916    |
            +-----------------------+-------------------+-------------------+
            | WBThrottle            |                   |                   |
            +-----------------------+-------------------+-------------------+
            | bytes_dirtied         | 40194316          | 40194316          |
            +-----------------------+-------------------+-------------------+
            | ios_dirtied           | 5                 | 5                 |
            +-----------------------+-------------------+-------------------+

###counters_timer.py

This module provides class CountersTimer, which can be used for to get counters difference after some operations.  

Supposed to use it in "with" statement.  

__init__ takes optional parameters:  

    perf_counters: dict with counters in format \{"collection":\["counter1", "counter2",...\]\}, if None (by default) - all counters will be used
    host: controller host, if you don't specify it, localhost will be used
    user: user for ligin, "root" by default

You get result as dict in format \{counter_name: \{node_name:counter_difference\}\}, where counter_name = collection.counter  

If you want to save counters list in several calls, use one instance of class.  

####Examples

Difference for all counters, list of counters was queried from ceph once:  

    ct = CountersTimer(host=some_host)
    with ct as result:
        time.sleep(10)
    print ("Diff after sleep 10: ", result.perf_difference)
    with ct as result:
        time.sleep(5)
    print ("Diff after sleep 5: ", result.perf_difference)

Difference for all counters, list of counters was  queried from ceph twice:  

    with CountersTimer(host=some_host) as result:
        time.sleep(10)
    print ("Diff after sleep 10: ", result.perf_difference)
    with CountersTimer(host=some_host) as result:
        time.sleep(5)
    print ("Diff after sleep 5: ", result.perf_difference)

Difference for specified counters:  

    perf_counters = {'WBThrottle': ['bytes_dirtied', 'ios_dirtied'],
                    'filestore': ['journal_latency', 'journal_queue_max_ops']}
    with CountersTimer(host=some_host, perf_counters=perf_counters) as result:
        time.sleep(10)
    print ("Diff after sleep 10: ", result.perf_difference)


    
