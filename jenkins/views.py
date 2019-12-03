# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import HttpResponse
from .core import Job, JobInfo
from python_jenkins.settings import JENKINS_PATH
from python_jenkins.settings import JENKINS_PORT
from python_jenkins.settings import JENKINS_USER
from python_jenkins.settings import JENKINS_PWD


def getversion(request):
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).getversion())


def getjoblist(request):
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).getjoblist())


def getconfig(request):
    jobname = request.GET.get('jobname', '')
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).getconfig(jobname))


def getjobstatus(request):
    jobname = request.GET.get('jobname', '')
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).getjobstatus(jobname))


def getbuildconsole(request):
    jobname = request.GET.get('jobname', '')
    buildnum = request.GET.get('buildnum', '')
    return HttpResponse(
        JobInfo(jobname=jobname, buildnum=buildnum, ip=JENKINS_PATH, uname=JENKINS_USER, pwd=JENKINS_PWD,
                port=JENKINS_PORT).getbuildonsole())


def postbuildnewjob(request):
    jobname = request.POST.get('jobname', '')
    config = request.POST.get('config', '')
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).initnewjob(jobname, config))


def getdownstream(request):
    jobname = request.GET.get('jobname', '')
    buildnum = request.GET.get('buildnum', '')
    return HttpResponse(
        JobInfo(jobname=jobname, buildnum=buildnum, ip=JENKINS_PATH, uname=JENKINS_USER, pwd=JENKINS_PWD,
                port=JENKINS_PORT).getdownstreambuild())


def getupstream(request):
    jobname = request.GET.get('jobname', '')
    buildnum = request.GET.get('buildnum', '')
    return HttpResponse(
        JobInfo(jobname=jobname, buildnum=buildnum, ip=JENKINS_PATH, uname=JENKINS_USER, pwd=JENKINS_PWD,
                port=JENKINS_PORT).getupstreambuild())


def getbuildobstatus(request):
    jobname = request.GET.get('jobname', '')
    buildnum = request.GET.get('buildnum', '')
    return HttpResponse(
        JobInfo(jobname=jobname, buildnum=buildnum, ip=JENKINS_PATH, uname=JENKINS_USER, pwd=JENKINS_PWD,
                port=JENKINS_PORT).getbuildobstatus())


def initial(request):
    return HttpResponse(Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).initialjob())


def start(request):
    jobname = request.POST.get('jobname', '')
    params = {}
    for i in request.POST.keys():
        if i != 'jobname':
            params[i] = request.POST.get(i, '')
    return HttpResponse(
        Job(JENKINS_PATH, JENKINS_USER, JENKINS_PWD, JENKINS_PORT).parambuild(jobname=jobname, params=params))
