# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
import json
from core import Job


def getVersion(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getVersion())


def getJobList(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getJobList())


def getConfig(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getConfig("pipeline_test"))


def getJobStatus(request):
    return HttpResponse(Job("192.168.1.150", "admin", "r00tme", "18080").getJobStatus("pipeline_test"))
