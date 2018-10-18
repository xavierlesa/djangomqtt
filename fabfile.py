#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'ubuntu'
env.sudo_user = 'ubuntu'
env.hosts = ['awswebhooks']
env.key_filename = ['~/.ssh/awsiot.pem']

def test_migrations():
    local("python manage.py makemigrations --dry-run --settings=djangomqtt.local")
    local("python manage.py migrate --list --settings=djangomqtt.local")

def make_migrations():
    local("python manage.py makemigrations --settings=djangomqtt.local")
    local("python manage.py migrate --settings=djangomqtt.local")

def prepare_deploy():
    with settings(warn_only=True):
        result = local("git add -p && git commit", capture=True)
    if result.failed and not confirm("git add & commit failed. Continue anyway?"):
        abort("Aborting at user request.")

    with settings(warn_only=True):
        result = local("git push", capture=True)
    if result.failed and not confirm("git push failed. Continue anyway?"):
        abort("Aborting at user request.")

def test_deploy():
    path = '/home/ubuntu/djangomqtt/'
    with cd(path), prefix('source /home/ubuntu/djangomqtt/env/bin/activate'):
        run('git pull')
        run('python manage.py makemigrations --dry-run --settings=djangomqtt.production')
        run('python manage.py migrate --list --settings=djangomqtt.production')

def deploy():
    path = '/home/ubuntu/djangomqtt/'
    with cd(path), prefix('source /home/ubuntu/djangomqtt/env/bin/activate'):
        run('git pull')
        run('python manage.py makemigrations --settings=djangomqtt.production')
        run('python manage.py migrate --settings=djangomqtt.production')

def server_restart():
    sudo("/etc/init.d/uwsgi restart", user="root")
