#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-02 20:08:05
import sys
import os
import time
import logging

from subprocess import PIPE, Popen

logging.basicConfig(filename="/data/proclog/log/fscs/rcms_issued.log", level=logging.DEBUG)

HAPROXY_HISTORY_CONFIG_DIRECTORY = '/usr/local/haproxy/etc/history_cfg'
TEMP_CONFIG_LOCATION = '/usr/local/haproxy/etc/haproxy.cfg.download'
BACKUP_CONFIG_LOCATION = '/usr/local/haproxy/etc/haproxy.cfg.backup'
NORMAL_CONFIG_LOCATION = '/usr/local/haproxy/etc/haproxy.cfg'
HAPROXY_LOCATION = '/usr/local/haproxy/sbin/haproxy'

################################################################################
command_dict = {
    ############################# reload_fscs_init  ####################################
    "backup_history_config" : ["cp %s %s" % (NORMAL_CONFIG_LOCATION, os.path.join(HAPROXY_HISTORY_CONFIG_DIRECTORY, "haproxy.conf_%s" % time.strftime("%y%m%d%H%M%S", time.localtime()))), ""],
    "prepare_fscs_config" : ["cp %s %s" % (os.path.join(os.getcwd(), "haproxy.cfg"), TEMP_CONFIG_LOCATION), ""],
    ############################# reload_fscs_config  ####################################
    "check_download_fscs_config" : ["%s -c -q -V -f %s" % (HAPROXY_LOCATION, TEMP_CONFIG_LOCATION), ""],
    "backup_fscs_config" : ["mv %s %s" % (NORMAL_CONFIG_LOCATION, BACKUP_CONFIG_LOCATION), ""],
    "copy_download_fscs_config_to_normal" : ["cp -av %s %s" % (TEMP_CONFIG_LOCATION, NORMAL_CONFIG_LOCATION), ""],
    "reload_fscs" : ["/etc/init.d/haproxy reload", ""],
    "restore_fscs_config" : ["mv %s %s" % (BACKUP_CONFIG_LOCATION, TEMP_CONFIG_LOCATION), ""],
}
err_list = []
result_list = []

def reload_fscs_init():
    if not os.path.exists(HAPROXY_HISTORY_CONFIG_DIRECTORY):
        os.mkdir(HAPROXY_HISTORY_CONFIG_DIRECTORY)

    run_command("backup_history_config")
    run_command("prepare_fscs_config")

def run_command(cmd_key):
    global result_list, err_list
    ''' return (return_code, script, stdout, stderr) '''
    cmd, args = command_dict[cmd_key]
    logging.info(cmd)
    pipe = Popen(cmd, shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE)
    pipe.stdin.write(args)
    pipe.stdin.flush()
    pipe.stdin.close()

    out = pipe.stdout.read()
    if out:
        logging.info(out)
        result_list.append(out)

    err = pipe.stderr.read()
    if err:
        logging.error(err)
        err_list.append(cmd)
        err_list.append(err)

def reload_fscs_config():
    global result_list, err_list
    err_list = []
    result_list = []

    run_command("check_download_fscs_config")
    if not err_list:
        run_command("backup_fscs_config")
        run_command("copy_download_fscs_config_to_normal")
        run_command("reload_fscs")
        if err_list:
            run_command("restore_fscs_config")

    if err_list:
        return sys.exit(1)
    return sys.exit(0)

if __name__ == "__main__":
    reload_fscs_init()
    reload_fscs_config()
