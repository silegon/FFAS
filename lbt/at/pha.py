#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-04 21:44:09

from collections import defaultdict

def get_file_data(at_id):
    file = "lbhash_%s.log" % at_id
    with open(file, 'r') as f:
        raw_data = f.read()

    dl = defaultdict(list)
    for i in raw_data.splitlines():
        server, url = i.split()
        dl.setdefault(server, []).append(url)
    return dl

def get_access_data(raw_at_id, diff_at_id):
    trd = get_file_data(raw_at_id)
    tdd = get_file_data(diff_at_id)
    strd_keys = set(trd.keys())
    stdd_keys = set(tdd.kesy())

    for i in strd_keys - stdd_keys:
        tdd[i] = []

    for i in stdd_keys - strd_keys:
        trd[i] = []
    return trd, tdd

def parse_data(trd, tdd):
    data = {}
    rdata = {}
    total_url_count = 0
    total_same_url_count = 0
    for item in sorted(trd.keys()):
        item_dict = {}
        trds = set(trd[item])
        tdds = set(tdd[item])
        server_same_url_count = len(trds | tdds)
        total_same_url_count += server_same_url_count
        trd_url_count = len(trds)
        total_url_count += trd_url_count
        tdd_url_count = len(tdds)
        item_dict = {
            "trd_url_count" : trd_url_count,
            "tdd_url_count" : tdd_url_count,
            "server_same_url_count" : server_same_url_count,
        }
        data[item] = item_dict

    for item in sorted(trd.keys()):
        ruc = item['trd_url_count']
        duc = item['tdd_url_count']
        suc = item['server_same_url_count']
        rr = "%s %s" % (ruc/total_url_count, ruc)
        dr = "%s %s" % (duc/total_url_count, duc)
        flow_count = duc - ruc
        flow_ratio = flow_count/total_url_count
        new_count = suc - total_same_url_count
        new_ratio = new_count/total_same_url_count
        peak = (1 + flow_ratio) * (1 + new_ratio)
        dc = "peak %s<br>flow %s %s<br>new %s %s" % (peak, flow_ratio, flow_count, new_ratio, new_count)
        sr = "%s %s" % (suc/total_same_url_count, suc)
        srr = "%s" % suc/ruc
        sdr = "%s" % suc/duc
        rdata[item] = {
            "rr":rr,
            "dr":dr,
            "dc":dc,
            "sr":sr,
            "srr":srr,
            "sdr":sdr,
        }
        return rdata
