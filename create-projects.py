#!/usr/bin/env python

import os
import sys
import jenkins
import yaml
import glob
import shutil
import jj

if len(sys.argv) < 2:
    print "Usage: %s <Jenkins-URL>" % sys.argv[0]
    exit(1)

URL=sys.argv[1]

jobs = jj.JenkinsJobs(URL)

templates = jobs.load_templates()

for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

    for job,nameformat in project['jobs'].iteritems():
        if job == BRANCH_BUILD_JOB:
            for branch in project['branches']:
                project['branch'] = branch
                jobname = nameformat % project
                jobxml = templates[job] % project
                jobs.create_or_update(jobname, jobxml)
                jobs.build(jobname)
        else:
            jobname = nameformat % project
            jobxml = templates[job] % project
            jobs.create_or_update(jobname, jobxml)


