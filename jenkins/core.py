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
        return json.dumps(self.server.version, indent=4)

    def getJobList(self):
        return json.dumps(self.server.keys(), indent=4)

    def getConfig(self, jobname):
        return json.dumps(xmltodict.parse(self.server[jobname].get_config(), encoding='utf-8'), indent=4)

    def getJobStatus(self, jobname):
        infolist = {}
        infolist['name'] = self.server[jobname].name
        infolist['description'] = self.server[jobname].get_description()
        infolist['running'] = self.server[jobname].is_running()
        infolist['enabled'] = self.server[jobname].is_enabled()
        return json.dumps(infolist, indent=4)

    def setConfig(self, config):
        jsdict = json.loads(config)
        print(xmltodict.unparse(jsdict, encoding='utf-8'))
        return

    def paramBuild(self, jobname, params):
        buildnum = self.server.build_job(jobname, params)
        return buildnum


class jobInfo(Job):
    def __init__(self, jobname, buildnum, **kwargs):
        """
        # self.server[jobname].__dict__['_data']
        {
            "_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob",
            "actions": [
                {},
                {
                    "_class": "com.cloudbees.plugins.credentials.ViewCredentialsAction"
                }
            ],
            "description": "",
            "displayName": "pipeline_test",
            "displayNameOrNull": null,
            "fullDisplayName": "pipeline_test",
            "fullName": "pipeline_test",
            "name": "pipeline_test",
            "url": "http://192.168.1.150:18080/job/pipeline_test/",
            "buildable": true,
            "builds": [
                {
                    "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                    "number": 2,
                    "url": "http://192.168.1.150:18080/job/pipeline_test/2/"
                },
                {
                    "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                    "number": 1,
                    "url": "http://192.168.1.150:18080/job/pipeline_test/1/"
                }
            ],
            "color": "blue",
            "firstBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 1,
                "url": "http://192.168.1.150:18080/job/pipeline_test/1/"
            },
            "healthReport": [
                {
                    "description": "Build stability: 1 out of the last 5 builds failed.",
                    "iconClassName": "icon-health-60to79",
                    "iconUrl": "health-60to79.png",
                    "score": 80
                }
            ],
            "inQueue": false,
            "keepDependencies": false,
            "lastBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 15,
                "url": "http://192.168.1.150:18080/job/pipeline_test/15/"
            },
            "lastCompletedBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 15,
                "url": "http://192.168.1.150:18080/job/pipeline_test/15/"
            },
            "lastFailedBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 11,
                "url": "http://192.168.1.150:18080/job/pipeline_test/11/"
            },
            "lastStableBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 15,
                "url": "http://192.168.1.150:18080/job/pipeline_test/15/"
            },
            "lastSuccessfulBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 15,
                "url": "http://192.168.1.150:18080/job/pipeline_test/15/"
            },
            "lastUnstableBuild": null,
            "lastUnsuccessfulBuild": {
                "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
                "number": 11,
                "url": "http://192.168.1.150:18080/job/pipeline_test/11/"
            },
            "nextBuildNumber": 16,
            "property": [
                {
                    "_class": "hudson.model.ParametersDefinitionProperty",
                    "parameterDefinitions": [
                        {
                            "_class": "hudson.model.StringParameterDefinition",
                            "defaultParameterValue": {
                                "_class": "hudson.model.StringParameterValue",
                                "name": "json",
                                "value": "first-stage"
                            },
                            "description": "",
                            "name": "json",
                            "type": "StringParameterDefinition"
                        },
                        {
                            "_class": "hudson.model.BooleanParameterDefinition",
                            "defaultParameterValue": {
                                "_class": "hudson.model.BooleanParameterValue",
                                "name": "first_stage",
                                "value": true
                            },
                            "description": "",
                            "name": "first_stage",
                            "type": "BooleanParameterDefinition"
                        },
                        {
                            "_class": "hudson.model.BooleanParameterDefinition",
                            "defaultParameterValue": {
                                "_class": "hudson.model.BooleanParameterValue",
                                "name": "second_stage",
                                "value": false
                            },
                            "description": "",
                            "name": "second_stage",
                            "type": "BooleanParameterDefinition"
                        }
                    ]
                }
            ],
            "queueItem": null,
            "concurrentBuild": true,
            "resumeBlocked": false
        }
        """
        super().__init__(**kwargs)
        for i in self.server[jobname].__dict__['_data']['builds']:
            if i['number'] == buildnum:
                self.obj = Build(i['url'], i['number'], self.server[jobname])
                break

    def getBuildConsole(self):
        return json.dumps(self.obj.get_console(), indent=4)

    def getDownstreamBuild(self):
        downstream = []
        for i in self.obj.get_console().split('\n'):
            if "Starting building:" in i:
                downstream.append({'name': i.split(' ')[2], 'buildnum': i.split(' ')[3].strip('#')})
        return json.dumps(downstream, indent=4)

    def getUpstreamBuild(self):
        upstream = {}
        upstream['name'] = self.obj.get_upstream_job().__dict__["name"]
        upstream['buildnum'] = self.obj.get_upstream_build_number()
        return json.dumps(upstream, indent=4)
