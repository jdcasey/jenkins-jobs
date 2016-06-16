#!/usr/bin/env python

import os
import sys
import glob
import jj

if len(sys.argv) < 2:
    print "Usage: %s <Jenkins-URL>" % sys.argv[0]
    exit(1)

URL=sys.argv[1]

jobs = jj.JenkinsJobs(URL)

projects = []
for yamlfile in glob.glob('projects/*.yaml'):
    project = jobs.load_project(yamlfile)

    if project.get('disabled') is True:
        print "Skipping disabled project: %(name)s" % project
        continue

    for job,nameformat in project['jobs'].iteritems():
        if job == jj.BRANCH_BUILD_JOB:
            for branch in project['branches']:
                project['branch'] = branch
                projects.append(nameformat % project)
        else:
            projects.append(nameformat % project)

existing = jobs.get_existing()
for job in existing:
	name = job['name']
	if name not in projects:
		print "Purging: %s" % name
		jobs.delete(name)
	else:
		print "Keeping: %s" % name
