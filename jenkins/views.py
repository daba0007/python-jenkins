# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from .core import Job, jobInfo


def getVersion(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getVersion())


def getJobList(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getJobList())


def getConfig(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getConfig("pipeline_test"))


def getJobStatus(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getJobStatus("pipeline_test"))


def getBuildConsole(request):
    return HttpResponse(jobInfo(jobname="pipeline_test", buildnum=14, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getBuildConsole())


def getDownstream(request):
    return HttpResponse(jobInfo(jobname="pipeline_test", buildnum=14, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getDownstreamBuild())


def getUpstream(request):
    return HttpResponse(jobInfo(jobname="second-stage-1", buildnum=5, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getUpstreamBuild())
