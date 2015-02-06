# ceph_perf_counters
Script to collect ceph counters from all osds and get some of them

You need to have ssh access for all ceph nodes. You can do it like this: 
    1. Put your .pub file (with public key) on Fuel node (like this, for example scp .ssh/id_rsa.pub root@<fuel_node>:/root/myrsa.pub)
    2. Next send it from Fuel node by ssh-copy-id on all nodes from 'fuel --env-id <env_id> node list' (or only to controller and ceph nodes)
I'm sure, there are better ways :)

Note, that now the most of options are setted directly in code, I will fix it later.

perfcollect.py - contains functions, directly examining nodes. 
	get_perf_dump_in_map - function, which returns perf dump for all osds in dict

get_perfs.py - program, which provide table output for optional counters. Counters are listed in code (temporary)

Using:

    python get_perfs.py [controller_host] [user_name]

        controller_host - ip of controller node, isn't required if you set it in source or want to use default
        user_name       - user name, via it you will access ssh, optional, "root" by default

        Output like this:
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
