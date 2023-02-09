# -*- coding: utf-8 -*-
from fabric.api import *


prod_server = 'mauriciol@web603.webfaction.com'

def prod():
    env.hosts = [prod_server]
    env.remote_app_dir = '~/webapps/imoveisfin/imoveisfinanciados'
    env.remote_apache_dir = '~/webapps/imoveisfin/apache2'


def commit():
    message = raw_input("Enter a git commit message:  ")
    local("git add -A && git commit -m \"%s\"" % message)
    local("git push origin master")
    print("Changes have been pushed to remote repository...")


def requirements():
    require('hosts', provided_by=[prod])
    run("cd %s; pip3.5 install --user -r requirements.txt" % env.remote_app_dir)

def migrate():
    require('hosts', provided_by=[prod])
    run("cd %s; python3.5 manage.py migrate" % env.remote_app_dir)

def collectstatic():
    require('hosts', provided_by=[prod])
    run("cd %s; python3.5 manage.py collectstatic --noinput" % env.remote_app_dir)


def restart():
    """Restart apache on the server."""
    require('hosts', provided_by=[prod])
    require('remote_apache_dir', provided_by=[prod])

    run("%s/bin/restart;" % (env.remote_apache_dir))


def deploy():
    require('hosts', provided_by=[prod])
    require('remote_app_dir', provided_by=[prod])

    # First lets commit changes to git
    #commit()
    # Get version to deploy
    # version = raw_input("Enter a version to deploy: ")
    # Now lets pull the changes to the server
    run("cd %s; git pull origin master" % env.remote_app_dir)
    #run("cd %s; git checkout %s" % (env.remote_app_dir, version))
    # Install requirements.txt
    requirements()
    migrate()
    # And lastly update static media files
    collectstatic()
    restart()
    print("Your app has been deployed on server")