#coding:utf-8

from base64 import urlsafe_b64decode
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from models import LBTestConfig

def get_haproxy_config(request):
    g = request.GET
    at_id = g.get("at_id")
    lb_test_config = LBTestConfig.objects.get(pk=at_id)
    context = {"server_config":lb_test_config.server_config}
    template_name = "at/haproxy.cfg_template"
    return render_to_response(template_name, context)

def report_lbresult(request):
    g = request.GET
    at_id = g.get("at_id")
    b64_statistical_result = g.get("b64_statistical_result")
    result = urlsafe_b64decode(str(b64_statistical_result))
    lb_test_config = LBTestConfig.objects.get(pk=at_id)
    lb_test_config.statistical_result = result
    lb_test_config.save()

    return StreamingHttpResponse('')

def lb_report(request):
    g = request.GET
    raw_at_id = g.get("raw_at_id")
    diff_at_id = g.get("diff_at_id")
    try:
        raw_at = LBTestConfig.objects.get(pk=raw_at_id)
        diff_at = LBTestConfig.objects.get(pk=diff_at_id)
    except:
        return StreamingHttpResponse('LoadBalance test case id error')

    rsc = raw_at.server_config
    dsc = diff_at.server_config
    if not rsc or not dsc:
        return StreamingHttpResponse('LoadBalance test case have not finish')

    context = {
        "raw_sever_config":rsc,
        "diff_server_config":dsc,
    }
    template_name = "at/lb_report.html"
    return render_to_response(template_name, context)
