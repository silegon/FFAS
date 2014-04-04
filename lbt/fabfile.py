#coding:utf-8
from fabric.api import *

TEST_SERVER_PORT = '8500'
TEST_SERVER_IP = '192.168.135.101'


"""
Local fabfile, only for local develop
"""

@task
@hosts("localhost")
def sts():
    """
    start test server
    """
    local("python -B /home/silegon/temp/lb_test/lbt/manage.py runserver %s:%s" % (TEST_SERVER_IP , TEST_SERVER_PORT))

@task
@hosts("localhost")
def sns():
    """
    start normal server
    """
    local("uwsgi -x /home/silegon/lb_test/lbt/extra/server/uwsgi_lbt.xml")


@task
@hosts("localhost")
def shell():
    local('python /home/silegon/temp/lb_test/lbt/manage.py shell')
