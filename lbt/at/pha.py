#!/usr/bin/env python
# coding: utf-8
# "zhoukh"<silegon@gmail.com> 2014-04-04 21:44:09

from collections import defaultdict
from django.conf import settings
from os.path import join
from operator import itemgetter

def get_file_data(at_id):
    file = join(settings.LBHASH_FILE_DIRECTORY, "lbhash_%s.log" % at_id)
    with open(file, 'r') as f:
        raw_data = f.read()

    dl = defaultdict(list)
    for i in raw_data.splitlines():
        server, url = i.split()
        dl.setdefault(server, []).append(url)
    return dl

def ratio(molecular, denominator):
    if not denominator:
        return 0
    return "%.2f%%" % (molecular*100.0/denominator)

def parse_data(trd, tdd):
    data = {}
    rdata = []
    total_url_count = 0
    total_same_url_count = 0
    for item in sorted(trd.keys()):
        item_dict = {}
        trds = set(trd[item])
        tdds = set(tdd[item])
        server_same_url_count = len(trds & tdds)
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

    for key, value_dict in data.items():
        ruc = value_dict['trd_url_count']
        duc = value_dict['tdd_url_count']
        suc = value_dict['server_same_url_count']
        rr = "%s %s" % (ratio(ruc, total_url_count), ruc)
        dr = "%s %s" % (ratio(duc, total_url_count), duc)
        flow_count = duc - ruc
        flow_ratio = ratio(flow_count, total_url_count)
        #new_count = suc - total_same_url_count
        new_count = duc - suc
        new_ratio = ratio(new_count, duc)
        #peak = (1 + flow_ratio) * (1 + new_ratio)
        peak = ratio(duc + duc - suc, ruc)
        #dc = "peak %s flow %s %s new %s %s" % (peak, flow_ratio, flow_count, new_ratio, new_count)
        sr = "%s %s" % (ratio(suc, total_same_url_count), suc)
        srr = "%s" % ratio(suc, ruc)
        sdr = "%s" % ratio(suc, duc)
        d = {
            "server":key,
            "rr":rr,
            "dr":dr,
            "dc_peak":peak,
            "dc_flow":"%s %s" % (flow_ratio, flow_count),
            "dc_new":"%s %s" % (new_ratio, new_count),
            "sr":sr,
            "srr":srr,
            "sdr":sdr,
        }
        rdata.append(d)
    total_info = {
        "total_url_count" : total_url_count,
        "total_same_url_count" : total_same_url_count,
        "total_ratio" : ratio(total_same_url_count, total_url_count),
    }
    vrdata = sorted(rdata, key=itemgetter("server"))

    return vrdata, total_info
def get_access_analytics_data(raw_at_id, diff_at_id):
    trd = get_file_data(raw_at_id)
    tdd = get_file_data(diff_at_id)
    strd_keys = set(trd.keys())
    stdd_keys = set(tdd.keys())

    for i in strd_keys - stdd_keys:
        tdd[i] = []

    for i in stdd_keys - strd_keys:
        trd[i] = []

    data, total_info = parse_data(trd, tdd)
    return data, total_info
