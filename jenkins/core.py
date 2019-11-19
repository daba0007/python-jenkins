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

    def paramBuild(self, jobname, params):
        buildnum = self.server.build_job(jobname, params)
        return buildnum


class jobInfo(Job):
    def __init__(self, jobname, buildnum, **kwargs):
        super(jobInfo, self).__init__(**kwargs)
        for i in self.server[jobname].__dict__['_data']['builds']:
            if i['number'] == buildnum:
                self.obj = Build(i['url'], i['number'], self.server[jobname])
                break

    def getBuildConsole(self):
        return json.dumps(self.obj.get_console())

    def getDownstreamBuild(self):
        downstream = []
        for i in self.obj.get_console().split('\n'):
            if "Starting building:" in i:
                print i
                downstream.append({'name': i.split(' ')[2], 'buildnum': i.split(' ')[3].strip('#')})
        return json.dumps(downstream)

    def getUpstreamBuild(self):
        print self.obj.get_upstream_build()
        print self.obj.get_upstream_build_number()
        print self.obj.get_upstream_job()
        return json.dumps(self.obj.get_upstream_build_number())
