#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from python_jenkins.settings import INITIAL_PATH
import xmltodict
import json
import os


def buildcheck(func):
    def wrapper(self, *args, **kw):
        if self.obj == "error":
            result = dict(message="the build num is beyond the last build num")
            return json.dumps(result, indent=4)
        return func(self, *args, **kw)

    return wrapper


class Job(object):
    """
    deal with job
    """

    def __init__(self, ip, uname, pwd, port="8080"):
        self.url = "http://" + ip + ":" + port + "/"
        self.server = Jenkins(self.url, username=uname, password=pwd)

    def getversion(self):
        """
        get jenkins version
        :return: string
        """
        return json.dumps(self.server.version, indent=4)

    def getjoblist(self):
        """
        get all job
        :return: list
        """
        return json.dumps(self.server.keys(), indent=4)

    def getconfig(self, jobname):
        """
        get job's config
        :param jobname: string
        :return: list

        # config.json(from xml to json)
        {
            "flow-definition": {
                "@plugin": "workflow-job@2.36",
                "actions": {
                    "org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction": {
                        "@plugin": "pipeline-model-definition@1.4.0"
                    },
                    "org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction": {
                        "@plugin": "pipeline-model-definition@1.4.0",
                        "jobProperties": null,
                        "triggers": null,
                        "parameters": null,
                        "options": null
                    }
                },
                "description": null,
                "keepDependencies": "false",
                "properties": {
                    "hudson.model.ParametersDefinitionProperty": {
                        "parameterDefinitions": {
                            "hudson.model.StringParameterDefinition": {
                                "name": "json",
                                "description": null,
                                "defaultValue": "first-stage",
                                "trim": "false"
                            },
                            "hudson.model.BooleanParameterDefinition": [
                                {
                                    "name": "first_stage",
                                    "description": null,
                                    "defaultValue": "true"
                                },
                                {
                                    "name": "second_stage",
                                    "description": null,
                                    "defaultValue": "false"
                                }
                            ]
                        }
                    }
                },
                "definition": {
                    "@class": "org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition",
                    "@plugin": "workflow-cps@2.76",
                    "script": "pipeline {\n   agent any\n\n   stages {\n      stage('First Stage') {\n        when {\n          environment name: 'first_stage',\n          value: 'true'\n        }\n        steps {\n          build job: 'first-stage-1', parameters: [booleanParam(name: 'run_build', value: 'true'), string(name: 'data', value: params.json)]\n        }\n      }\n      stage('Second Stage') {\n        when {\n          environment name: 'second_stage',\n          value: 'true'\n        }\n        steps {\n          build job: 'second-stage-1', parameters: [booleanParam(name: 'run_build', value: 'true'), string(name: 'data', value: params.json)]\n        }\n      }\n   }\n}",
                    "sandbox": "true"
                },
                "triggers": null,
                "disabled": "false"
            }
        }
        path = os.path.join("initial", jobname + ".json")
        with open(path, 'w') as f:
            json.dump(xmltodict.parse(self.server[jobname].get_config(), encoding='utf-8'), f)
        """
        if self.server.has_job(jobname):
            return json.dumps(xmltodict.parse(self.server[jobname].get_config(), encoding='utf-8'), indent=4)
        else:
            result = dict(message="there is no such job")
            return json.dumps(result, indent=4)

    def getjobstatus(self, jobname):
        """
        get job's status
        :param jobname: string
        :return:
        """
        if self.server.has_job(jobname):
            result = dict(name=self.server[jobname].name, description=self.server[jobname].get_description(),
                          running=self.server[jobname].is_running(), enabled=self.server[jobname].is_enabled())
            return json.dumps(result, indent=4)
        else:
            result = dict(message="there is no such job")
            return json.dumps(result, indent=4)

    def getlastbuid(self, jobname):
        """
        :param jobname:
        :return: type(int)
        """
        if self.server.has_job(jobname):
            return json.dumps(self.server[jobname].get_last_good_build().__dict__['buildno'], indent=4)
        else:
            result = dict(message="there is no such job")
            return json.dumps(result, indent=4)

    def parambuild(self, jobname, params):
        """
        create new job
        :param jobname: string
        :param params: dict
        :return:
        """
        if self.server.has_job(jobname):
            job = self.server[jobname].invoke(build_params=params)
            if job.is_running() or job.is_queued():
                job.block_until_complete()
            return json.dumps(dict(number=job.__dict__['_data']['executable']['number']), indent=4)
        else:
            result = dict(message="there is no such job")
            return json.dumps(result, indent=4)

    def initnewjob(self, jobname, config):
        """
        create new job
        :param jobname: string
        :param config: json
        :return: string
        """
        self.server.create_job(jobname, xmltodict.unparse(json.loads(config), encoding='utf-8'))
        return jobname

    def initialjob(self):
        result = dict(filelist=os.listdir(INITIAL_PATH))
        for i in os.listdir(INITIAL_PATH):
            jobname = i.replace('.json', '')
            if jobname not in json.loads(self.getjoblist()):
                with open(INITIAL_PATH + i, 'r') as f:
                    job_dict = json.load(f)
                    self.server.create_job(jobname, xmltodict.unparse(job_dict, encoding='utf-8').encode())
        return json.dumps(result, indent=4)


class JobInfo(Job):
    """
    deal with builded job info
    """

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
            if i['number'] == int(buildnum):
                self.obj = Build(i['url'], i['number'], self.server[jobname])
                break

    def __getattr__(self, attr):
        if attr == 'obj':
            return "error"

    @buildcheck
    def getbuildconsole(self):
        """
        get all console from job
        :return: json
        """
        return json.dumps(self.obj.get_console(), indent=4)

    @buildcheck
    def getdownstreambuild(self):
        """
        get downstream job list
        :return: json
        """
        result = []
        for i in self.obj.get_console().split('\n'):
            if "Starting building:" in i:
                result.append({'name': i.split(' ')[2], 'buildnum': i.split(' ')[3].strip('#')})
        return json.dumps(result, indent=4)

    @buildcheck
    def getupstreambuild(self):
        """
        get upstream job
        :return: json
        """
        result = dict(name=self.obj.get_upstream_job().__dict__["name"], buildnum=self.obj.get_upstream_build_number())
        return json.dumps(result, indent=4)

    @buildcheck
    def getbuildobstatus(self):
        """
        get builded-job status
        :return: json
        """
        return json.dumps(self.obj.get_status(), indent=4)
