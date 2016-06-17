#!/usr/bin/env python

import os
import sys
import glob
import jj
import optparse

parser = optparse.OptionParser()

parser.add_option('-C', '--config', help='Use an alternative configuration (default: {secrets})'.format(secrets=jj.DEFAULT_CONFIG_FILE))
parser.add_option('-G', '--generate-only', action='store_true', help='Only generate the job XML files, don\'t update Jenkins.')
parser.add_option('-T', '--trigger', action='store_true', help='Trigger builds')

opts, args = parser.parse_args()

print "Setting up Jenkins connection"
jobs = jj.JenkinsJobs(opts.config)

print "Reading templates"
templates = jobs.load_templates()

print "Processing project configurations"

for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

    print "Processing branch configs for: %s" % project['name']
    for branch in project['branches']:
        branchName = str(branch[jj.BRANCH_NAME])
        project[jj.BRANCH_NAME] = branchName
        project[jj.BUILD_COMMAND] = branch[jj.BUILD_COMMAND]

        jobname = branch[jj.NAME_FORMAT] % project
        jobxml = templates[branch.get(jj.TEMPLATE_NAME) or jj.BRANCH_BUILD_JOB] % project
        stored = jobs.create_or_update(jobname, jobxml, not opts.generate_only)
        if stored is True and opts.trigger is True:
            jobs.build(jobname)

    print "Processing PR branch config for: %s" % project['name']
    prBranch = project[jj.PR_BUILD_JOB]
    if prBranch is not None:
        project[jj.BUILD_COMMAND] = prBranch[jj.BUILD_COMMAND]
        jobname = prBranch[jj.NAME_FORMAT] % project
        jobxml = templates[prBranch.get(jj.TEMPLATE_NAME) or jj.PR_BUILD_JOB] % project
        jobs.create_or_update(jobname, jobxml, not opts.generate_only)


