#import wingdbstub
import time
import os, sys
#import pexpect
from fabric.api import local, cd, run, env, sudo, require
from flask_seed.local_settings import Config

fab            = Config.FABRIC['live']

env.hosts      = fab['HOSTS']
env.user       = fab['ADMIN_USER']
env.admin_     = fab['ADMIN_USER']
env.admin_user = fab['ADMIN_USER']
env.password   = fab['ADMIN_PW']

# def deploy(push_code=False):
def deploy(msg="No Msg"):
    #if push_code:
        #commit_code()
    commit(msg)
    update_remote()
    run_tests()
    reload_uwsgi()


def commit(msg):
    with cd(os.path.abspath(os.path.dirname(__file__))):
        local('git add .')
        local('git commit -am"%s"' % msg)
        local('git push origin master') # push local to repository

def update_remote():
    env.user       = fab['WEB_USER']
    with cd(fab['PROJECT_ROOT']):
        run('git pull origin master') # pull from repository to remote

# def run_tests():
#     with cd(fab['PROJECT_ROOT']):
#         run('export PYTHONPATH=/srv/gs/api/flask_seed/:/srv/gs/api/flask_seed/venv/lib/python2.7/site-packages/ && nosetests tests') 

# def r():
#     # symlink convenience
#     # ln -s /home/flt/django/projects/flt/ /home/flt/dj
#     run('cd C:\Users\Larry\__prjs\flt; ls')


#from fabric.decorators import runs_once

from fabric.contrib.console import confirm

# see: http://blog.tplus1.com/index.php/2010/12/31/how-to-restart-a-gunicorn-server-from-vim/
def reload_code():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill -HUP `cat gunicorn.pid`')

def start_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('python manage.py run_gunicorn -c gunicorn.conf.py --traceback 0.0.0.0:8001')

def stop_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill `cat gunicorn.pid`')


def restart_gunicorn():
    with cd(fab['PROJECT_ROOT']):
        sudo('kill `cat gunicorn.pid`')
        sudo('python manage.py run_gunicorn -c gunicorn.conf.py --traceback 0.0.0.0:8001')

def reload_uwsgi():
    sudo('pkill -9 uwsgi')

def reload_uwsgi():
    with cd(fab['PROJECT_ROOT']):
        run('pkill -9 uwsgi')

def reload_nginx_conf():
    sudo('/etc/init.d/nginx check')
    sudo('/etc/init.d/nginx reload')

def restart():
    sudo('supervisorctl restart ourfield')
    # sudo /etc/init.d/nginx restart
    sudo('/etc/init.d/nginx restart')


def pushpull():
    local('git push') # runs the command on the local environment
    run('cd /path/to/project/; git pull') # runs the command on the remote environment



# the following is fab file from another project
# from fabric.api import run, env, cd, sudo


# def production():
#     env.hosts = ['yourhost.com']
#     env.repo = ('/srv/yourproject/', 'origin', 'master')


# def git_pull(hash=None):
#     """Updates or resets the repository"""
#     repo, parent, branch = env.repo
#     if hash is None:
#         hash = '%s/%s' % (parent, branch)
#     with cd(repo):
#         run('git fetch')
#         run('git reset --hard %s' % hash)


# def buildout():
#     repo, parent, branch = env.repo
#     with cd(repo):
#         run('./bin/buildout')


# def deploy(hash=None):
#     repo, parent, branch = env.repo
#     git_pull(hash)
#     buildout()
#     with cd(repo):
#         run('./bin/django syncdb')
#     restart_supervisor()


# def reset(hash):
#     deploy(hash)


# def restart_nginx():
#     sudo('/etc/init.d/nginx restart')


# def restart_supervisor():
#     sudo('supervisorctl restart all')
