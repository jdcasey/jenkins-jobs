import os
import sys
import jenkins
import yaml
import glob
import shutil

BRANCH_BUILD_JOB='branch-build'
PR_BUILD_JOB='pr-build'
GENERATED_XML = "generated-xml"
SECRETS=os.path.join(os.getenv("HOME"), ".jenkins-secrets.yaml")
DEFAULTS=os.path.join(os.getcwd(), 'defaults.yaml')

class JenkinsJobs(object):
    def __init__(self, url):
        self.url = url

        self.secrets = {}
        if os.path.exists(SECRETS):
            with open(SECRETS) as f:
                self.secrets = yaml.load(f)
        else:
            raise "No secrets file found at: %s!" % SECRETS

        if 'username' not in self.secrets or 'token' not in self.secrets:
            raise "Secrets file must contain Jenkins 'username' and 'token'"

        self.server = jenkins.Jenkins(self.url, username=self.secrets['username'], password=self.secrets['token'])
        self.secrets.pop('token', None)

        generated_dir = os.path.join(os.getcwd(), GENERATED_XML)
        if os.path.isdir(generated_dir):
            shutil.rmtree(generated_dir)
        os.makedirs(generated_dir)

    def load_project(self, yaml_file):
        init_defaults()
        project = self.defaults.copy()
        project.update(secrets)
        with open(yamlfile) as f:
            project.update(yaml.load(f))
        return project

    def init_defaults(self):
        if self.defaults is not None:
            return self.defaults

        self.defaults={}
        if os.path.exists(DEFAULTS):
            with open(DEFAULTS) as f:
                self.defaults = yaml.load(f)
        else:
            print "WARNING: No defaults found at: %s" % DEFAULTS

        return self.defaults

    def load_templates(self):
        if self.templates is not None:
            return self.templates

        self.templates = {}
        for templatefile in glob.glob('templates/*.xml'):
            key = os.path.splitext(os.path.basename(templatefile))[0]
            with open(templatefile) as f:
                self.templates[key] = f.read()
        return self.templates

    def create_or_update(self, name, jobxml):
        with open(os.path.join(generated_dir, "%s.xml" % name), 'w') as f:
            f.write(jobxml)

        try:
            if server.job_exists(name) is True:
                print "Updating: %s" % name
                self.server.reconfig_job(name, jobxml)
            else:
                print "Creating: %s" % name
                self.server.create_job(name, jobxml)
            return True
        except jenkins.JenkinsException as e:
            print "Failed: %s" % e
        return False

    def build(self, name):
        print "Triggering rebuild of: %s" % name
        self.server.build_job(name)


