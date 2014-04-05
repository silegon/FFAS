#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-03 04:02:59

import os
from fabric.api import *
from urllib import urlopen, urlretrieve
from base64 import urlsafe_b64encode

env.hosts = [
    "root@192.168.135.103",
]

env.passwords = {
    "root@192.168.135.103:22":"root",
}

#@task
#def run_lb_test(number):
#    remote_clear()
#    getconfig()
#    use_config()
#    run_remote_test()
#    get_halog_srv()
#    get_accesslog_result()
#    get_back_result_file()
#    report_task()
REMOTE_WORKING_DIRECTORY = "/root/lbt"
REMOTE_HALOG_DIRECTORY = os.path.join(REMOTE_WORKING_DIRECTORY, "halog")
REMOTE_LBHASH_DIRECTORY = os.path.join(REMOTE_WORKING_DIRECTORY, "lbhash")
REMOTE_HAPROXY_LOG = "/data/proclog/log/fscs/access.log"

LOCAL_PROJECT_DIRECTORY = "/home/silegon/lb_test/lbr"
LOCAL_HAPROXY_CFG_DIRECTORY = "/home/silegon/lb_test/lbr/haproxy_cfg"
LOCAL_HALOG_DIRECTORY = "/home/silegon/lb_test/lbr/halog"
LOCAL_LBHASH_DIRECTORY = "/home/silegon/lb_test/lbr/lbhash"

LOCAL_SITE = "http://192.168.135.101:8500/"

HAPROXY_CFG_URL = LOCAL_SITE + "get_haproxy_config?at_id=%s"
REPORT_URL = LOCAL_SITE + "report_lbresult?at_id=%s&b64_statistical_result=%s"

@task
@hosts("root@192.168.135.103")
def run_lb_test(at_id):
    #remote_clear
    run("rm %s && touch %s " % (REMOTE_HAPROXY_LOG, REMOTE_HAPROXY_LOG))
    run("mkdir -p %s" % REMOTE_HALOG_DIRECTORY)
    run("mkdir -p %s" % REMOTE_LBHASH_DIRECTORY)

    local_haproxy_cfg_path = os.path.join(LOCAL_HAPROXY_CFG_DIRECTORY, "haproxy_%s.cfg" % at_id)

    print HAPROXY_CFG_URL % at_id
    urlretrieve(HAPROXY_CFG_URL % at_id, local_haproxy_cfg_path)
    put(local_haproxy_cfg_path, os.path.join(REMOTE_WORKING_DIRECTORY, "haproxy.cfg"))

    remote_reload_script = os.path.join(REMOTE_WORKING_DIRECTORY, "fscs_reload_config.py")
    local_reload_script = os.path.join(LOCAL_PROJECT_DIRECTORY, "fscs_reload_config.py")
    put(local_reload_script, remote_reload_script)
    run("python %s" % remote_reload_script)

    remote_request_script = os.path.join(REMOTE_WORKING_DIRECTORY, "lb_request.py")
    local_request_script = os.path.join(LOCAL_PROJECT_DIRECTORY, "lb_request.py")
    put(local_request_script, remote_request_script)
    run("python %s" % remote_request_script)

    lbhash_file = "lbhash_%s.log" % (at_id)
    remote_lbhash_file = os.path.join(REMOTE_LBHASH_DIRECTORY, lbhash_file)
    run("cat %s | awk '{print $9,$20}' > %s" % (REMOTE_HAPROXY_LOG, remote_lbhash_file))
    halog_file = "halog_%s.log" % (at_id)
    remote_halog_file = os.path.join(REMOTE_HALOG_DIRECTORY, halog_file)
    run("halog -srv > %s" % remote_halog_file)

    local_lbhash_file = os.path.join(LOCAL_LBHASH_DIRECTORY, lbhash_file)
    local_halog_file = os.path.join(LOCAL_HALOG_DIRECTORY, halog_file)
    get(remote_lbhash_file, local_lbhash_file)
    get(remote_halog_file, local_halog_file)

    hf = open(local_halog_file, 'r')
    b64_halog_data = urlsafe_b64encode(hf.read())
    hf.close()
    report_url = REPORT_URL % (at_id, b64_halog_data)
    urlopen(report_url)
