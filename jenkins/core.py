#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
import xmltodict
import json


class Job(object):
    """
    deal with job
    """

    def __init__(self, ip, uname, pwd, port="8080"):
        self.url = "http://" + ip + ":" + port + "/"
        self.server = Jenkins(self.url, username=uname, password=pwd)

    def getVersion(self):
        return json.dumps(self.server.version)

    def getJobList(self):
        return json.dumps(self.server.keys())

    def getConfig(self, jobname):
        return json.dumps(xmltodict.parse(self.server[jobname].get_config(), encoding='utf-8'), indent=4)

    def getJobStatus(self, jobname):
        infolist = {}
        infolist['name'] = self.server[jobname].name
        infolist['description'] = self.server[jobname].get_description()
        infolist['running'] = self.server[jobname].is_running()
        infolist['enabled'] = self.server[jobname].is_enabled()
        return json.dumps(infolist)

    def setConfig(self, config):
        jsdict = json.loads(config)
        print xmltodict.unparse(jsdict, encoding='utf-8')
        return
