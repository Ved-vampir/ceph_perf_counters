#!/usr/local/bin/python

from __future__ import with_statement
import json
from fabric import tasks
from fabric.api import env, run, hide, settings, task
from fabric.network import disconnect_all


default_user = 'root' # via him you enter the host
cnt_host = '172.16.54.71' # controller host - you need set it!

def osds_list_task():
# gets list og osds id
    osd_list = run('ceph osd ls').split('\n') # osd ids list
    return osd_list

@task
def osds_ips_task(osd_list):
# get osd's ips
    ips = []
    for osd_id in osd_list:
        ips.append (json.loads (run('ceph osd find '+osd_id))["ip"].split(":")[0]) # find hosts
    return ips


def get_perf_dump_task():
# get perf dump for one osd
    osd_name = run ('ls /var/run/ceph/ |grep .asok')
    perf_list = json.loads (run('ceph --admin-daemon /var/run/ceph/'+osd_name+' perf dump'))
    return perf_list

def get_perf_dump_in_map(host=cnt_host, user=default_user):
# this function do all work
    with hide('output','running','warnings','status'), settings(warn_only=True): # for disable fabric output
        print ("Collecting.....") # this is not very fast

        # go to ceph on controller for osd's ips
        env.user = user
        env.hosts = [host]
        osd_lists = tasks.execute(osds_list_task)[env.hosts[0]]
        ip_list = tasks.execute(osds_ips_task, osd_list=osd_lists)[env.hosts[0]]

        # set hosts for osds and gateway (ips are local)
        env.hosts = ip_list
        env.gateway = cnt_host

        perf_list = tasks.execute(get_perf_dump_task)

        disconnect_all()

        k = 0
        perf_list_named = {"osd"+osd_lists[k]: e[1] for k, e in enumerate(perf_list.items())} # change names in map for to find them by osds
        # for key, pd in perf_list.items():
        #    perf_list_named["osd"+osd_lists[k]] = pd
        #    k+=1

        return perf_list_named

def main(): # just for test
    perf_list = get_perf_dump_in_map ()

    print perf_list


if __name__ == '__main__':
    main()
