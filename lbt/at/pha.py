#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-04 21:44:09

from collections import defaultdict

with open("lbhash_1.log") as f1:
    d1 = f1.read()

with open("lbhash_2.log") as f2:
    d2 = f2.read()

ds1 = defaultdict(list)

ds2 = defaultdict(list)

for i in d1.splitlines():
    server, url = i.split()
    ds1.setdefault(server, []).append(url)

for i in d2.splitlines():
    server, url = i.split()
    ds2.setdefault(server, []).append(url)

for item in sorted(ds1.keys()):
    print "server: %s" % item
    dss1 = set(ds1[item])
    dss2 = set(ds2[item])
    td1 = len(dss1)
    td2 = len(dss2)

    same = len(dss1 & dss2)
    print "same url: %s " % same
    print "mode1 : %s %s%%" % (len(dss1), same*100/td1)
    print "mode2 : %s %s%%" % (len(dss2), same*100/td2)
    print
