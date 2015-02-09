# ceph_perf_counters
Script to collect ceph counters from all osds and get some of them.

You need to have ssh access for all ceph nodes. 
You can do it manually like this: 
    1. Put your .pub file (with public key) on Fuel node (like this, for example scp .ssh/id_rsa.pub root@<fuel_node>:/root/myrsa.pub)
    2. Next send it from Fuel node by ssh-copy-id on all nodes from 'fuel --env-id <env_id> node list' (or only to controller and ceph nodes)
Or you can use script ./get_access.sh <fuel_host> <environment_name>. This script uses algorithm, described above. You need to know root password of fuel host and to have local rsa key, named id_rsa. Note, that it is only for convenience, it can be not very safe or have any other problems. Read script for additional information.
I'm sure, there are better ways :)


perfcollect.py - contains functions, directly examining nodes. 
	get_perf_dump_in_map(host=cnt_host, user=default_user) - function, which returns perf dump for all osds in dict, it takes two optional parameters: controller host node and user name (root by default).

get_perfs.py - program, which provide table output for optional counters. Counters are listed in code (temporary)

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

    Note, if you don't use one of -c or -g options, counter names from the code will be used.

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
