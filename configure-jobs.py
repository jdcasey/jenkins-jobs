#!/usr/bin/env python

import os
import sys
import glob
import jj
import optparse

parser = optparse.OptionParser()

parser.add_option('-C', '--config', help='Use an alternative configuration (default: {secrets})'.format(secrets=jj.SECRETS))
parser.add_option('-T', '--trigger', action='store_false', help='Trigger builds')

opts, args = parser.parse_args()

jobs = jj.JenkinsJobs(opts.config)

templates = jobs.load_templates()

for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

    for job,nameformat in project['jobs'].iteritems():
        if job == jj.BRANCH_BUILD_JOB:
            for branch in project['branches']:
                project['branch'] = branch
                jobname = nameformat % project
                jobxml = templates[job] % project
                jobs.create_or_update(jobname, jobxml)
                if opts.trigger is True:
                    jobs.build(jobname)
        else:
            jobname = nameformat % project
            jobxml = templates[job] % project
            jobs.create_or_update(jobname, jobxml)


