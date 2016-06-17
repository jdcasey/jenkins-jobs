#!/usr/bin/env python

import os
import sys
import glob
import jj
import optparse

parser = optparse.OptionParser()

parser.add_option('-C', '--config', help='Use an alternative configuration (default: {secrets})'.format(secrets=jj.SECRETS))
opts, args = parser.parse_args()

jobs = jj.JenkinsJobs(opts.config)

for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

    for job,nameformat in project['jobs'].iteritems():
        if job == jj.BRANCH_BUILD_JOB:
            for branch in project['branches']:
                project['branch'] = branch
                jobs.build(nameformat % project)
