#!/usr/bin/env python

import os
import sys
import requests
import yaml

if len(sys.argv) < 2:
    print "Usage: %s <org-name>" % sys.argv[0]
    exit(1)

PROJECTS = os.path.join(os.getcwd(), 'projects')
REPO_LIST_URL='https://api.github.com/orgs/%(org)s/repos'
ORG = sys.argv[1]

url=REPO_LIST_URL % {'org': ORG}
print "Getting repos from: %s" % url
r=requests.get(url)
if r.status_code != requests.codes.ok:
    print "Failed to retrieve repo list for: %s" % ORG
    exit(1)

if os.path.isdir(PROJECTS) is False:
    os.makedirs(PROJECTS)

repos=r.json()
for repo in repos:
    name=str(repo['name'])
    project = {
        'name': name,
        'github-url': str(repo['html_url'])
    }

    fname=os.path.join(PROJECTS, "%s.yaml" % name)
    print "Writing: %s" % fname
    with open(fname, 'w') as f:
        f.write(yaml.dump(project, default_flow_style=False))
