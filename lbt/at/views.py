#coding:utf-8

from base64 import urlsafe_b64decode
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from models import LBTestConfig

def get_haproxy_config(request):
    g = request.GET
    at_id = g.get("at_id")
    lb_test_config = LBTestConfig.models.get(pk=at_id)
    context = {"server_config":lb_test_config.server_config}
    template_name = "at/haproxy.cfg_tempalte"
    return render_to_response(template_name, context)

def report_lbresult(request):
    g = request.GET
    at_id = g.get("at_id")
    b64_statistical_result = g.get("b64_statistical_result")
    lb_test_config = LBTestConfig.models.get(pk=at_id)
    lb_test_config.statistical_result = urlsafe_b64decode(b64_statistical_result)
    lb_test_config.save()

    return StreamingHttpResponse('')
