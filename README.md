# ceph_perf_counters
Script to collect ceph counters from all osds and get some of them

You need to have ssh access for all ceph nodes. 

Note, that now all options are setted directly in code, I will fix it later.

perfcollect.py - contains functions, directly examining nodes. 
	get_perf_dump_in_map - function, which returns perf dump for all osds in dict

get_perfs.py - program, which provide table output for optional counters. Counters are listed in code (temporary)