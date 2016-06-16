# Jenkins Jobs

This repository contains scripts and YAML definitions to allow easy maintenance of Jenkins jobs for one or more GitHub organizations. In principle, you could also hand-author the YAML and use any Git repositories.

## Scanning An Organization

```
    $ ./scan-org-repos.py Commonjava
```

This will retrieve all the public repositories for the Commonjava organization. From these definitions, it will pull the 'name' and 'html_url' fields and use them to create a basic YAML file for each project.

## Creating / Updating Jenkins Jobs

Once you have your YAML definitions in place, you can push the new / updated job definitions using:

```
    $ ./create-projects.py http://my.jenkins.host
```

## Secrets

Your username, Jenkins API Token, and the GitHub API token registered for use with your Jenkins instance should be stored in `$HOME/.jenkins-secrets.yaml` with the following format:

```
    secret-gitHubAuthId: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    username: myuser
    token: 'xxxxxxxxxxxxxxxxxxxx'
```
