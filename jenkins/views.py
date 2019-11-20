# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse
from .core import Job, JobInfo


def getversion(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getversion())


def getjoblist(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getjoblist())


def getconfig(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getconfig("pipeline_test"))


def getjobstatus(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getjobstatus("pipeline_test"))


def getbuildconsole(request):
    return HttpResponse(JobInfo(jobname="pipeline_test", buildnum=14, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getBuildConsole())


def postbuildnewjob(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").initnewjob("new_pipeline_test",
                                                                                    Job("192.168.1.150", "admin",
                                                                                        "r00tme", "18080").getconfig(
                                                                                        "pipeline_test")))


def getdownstream(request):
    return HttpResponse(JobInfo(jobname="pipeline_test", buildnum=14, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getDownstreamBuild())


def getupstream(request):
    return HttpResponse(JobInfo(jobname="second-stage-1", buildnum=5, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getUpstreamBuild())


def getbuildobstatus(request):
    return HttpResponse(JobInfo(jobname="pipeline_test", buildnum=11, ip="192.168.1.150", uname="admin", pwd="r00tme",
                                port="18080").getBuildobStatus())
