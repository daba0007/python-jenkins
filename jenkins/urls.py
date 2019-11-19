#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^getversion', views.getVersion, name='getversion'),
    url(r'^getjoblist', views.getJobList, name='getjobList'),
    url(r'^getconfig', views.getConfig, name='getconfig'),
    url(r'^getjobstatus', views.getJobStatus, name='getjobStatus'),
    url(r'^getbuildconsole', views.getBuildConsole, name='getbuildconsole'),
    url(r'^getdownstream', views.getDownstream, name='getdownstream'),
    url(r'^getupstream', views.getUpstream, name='getupstream')
]
