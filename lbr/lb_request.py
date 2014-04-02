#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-03 03:13:58

import time

from urllib2 import urlopen

def lb_test_request():
    for i in range(10000):
        #res = urlopen("http://192.168.8.147:8500/%s" % i)
        res = urlopen("http://192.168.100.166/%s" % i)
        if res.read() != "echo":
            print "error"

if __name__ == "__main__":
    start_time = time.time()
    lb_test_request()
    print "spend_time:%s" % (time.time() - start_time)
