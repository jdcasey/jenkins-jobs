#!/usr/bin/env python

import os
import sys
import glob
import jj
import optparse

parser = optparse.OptionParser()

parser.add_option('-C', '--config', help='Use an alternative configuration (default: {secrets})'.format(secrets=jj.DEFAULT_CONFIG_FILE))
parser.add_option('-T', '--trigger', action='store_false', help='Trigger builds')

opts, args = parser.parse_args()

jobs = jj.JenkinsJobs(opts.config)

templates = jobs.load_templates()

for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

        for branch in project['branches']:
            project[jj.BRANCH_NAME] = branch['name']
            project[jj.BUILD_COMMAND] = branch[BUILD_COMMAND]

            jobname = nameformat % project
            jobxml = templates[branch.get(jj.TEMPLATE_NAME) or jj.BRANCH_BUILD_JOB] % project
            jobs.create_or_update(jobname, jobxml)
            if opts.trigger is True:
                jobs.build(jobname)

        prBranch = project[jj.PR_BUILD_JOB]
        if prBranch is not None:
            project[jj.BUILD_COMMAND] = prBranch[jj.BUILD_COMMAND]
            jobname = nameformat % project
            jobxml = templates[prBranch.get(jj.TEMPLATE_NAME) or jj.PR_BUILD_JOB] % project
            jobs.create_or_update(jobname, jobxml)


