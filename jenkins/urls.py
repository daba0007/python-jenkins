#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getversion', views.getversion, name='getversion'),
    url(r'^getjoblist', views.getjoblist, name='getjobList'),
    url(r'^getconfig', views.getconfig, name='getconfig'),
    url(r'^getjobstatus', views.getjobstatus, name='getjobStatus'),
    url(r'^getbuildconsole', views.getbuildconsole, name='getbuildconsole'),
    url(r'^getdownstream', views.getdownstream, name='getdownstream'),
    url(r'^getupstream', views.getupstream, name='getupstream'),
    url(r'^getbuildobstatus', views.getbuildobstatus, name='getbuildobstatus'),
    url(r'^getbuildobstatus', views.getbuildobstatus, name='getbuildobstatus'),

    url(r'^initial', views.initial, name='initial'),
]
