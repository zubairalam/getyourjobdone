import crypt
import os

from fabric.api import settings, lcd, task
from fabric.context_managers import prefix
from fabric.operations import local as lrun, run, sudo
from fabric.state import env
from StringIO import StringIO

home_path = '/home/firethoughts/'
www_path = '/var/www/www.firethoughts.mu'


@task
def local():
    """
    local machine config
    """
    env.run = lrun
    env.sudo = sudo
    env.hosts = ['localhost']


@task
def production():
    """
    production machine config
    """
    env.run = run
    env.sudo = sudo
    env.hosts = ['www.firethoughts.mu']


@task
def clean_cache():
    """
    clears system cache
    """
    env.run("free -m | awk 'FNR == 2 { print $4 }'")
    env.sudo("echo 3 > /proc/sys/vm/drop_caches")
    env.run("free -m | awk 'FNR == 2 { print $4 }'")


@task
def clean_memcached():
    """
    clears memcached
    """
    env.run("echo 'flush_all' | nc localhost 11211")


@task
def clean_files():
    """
    cleans files
    """
    with lcd(home_path):
        env.run("find . -name '*.pyc' -print0|xargs -0 rm -rf", capture=False)


@task
def kill(port=3000):
    """
    kills running processes
    """
    env.run("fuser -k {}/tcp".format(port))


@task
def clean():
    """
    removes unnecessary files
    """
    clean_cache()
    clean_memcached()
    clean_files()


@task
def report():
    """
    checks disk usage
    """
    disk_usage_io = StringIO()
    varnish_usage_io = StringIO()
    disk_usage = env.run("time df | awk 'FNR == 2 { print $5 }'", stdout=disk_usage_io)
    varnish_usage = env.run("varnishstat", stdout=varnish_usage_io)
    print("Current disk usage is {}".format(disk_usage))
    print("Current varnish usage is {}".format(varnish_usage))

@task
def generate_password(password):
    # python -c 'import crypt; print crypt.crypt("password", "$6$salt")'
    print(crypt.crypt("{}", "$6$salt").format(password))

@task
def refresh():
    """
    Refresh Server Environment
    """
    env.sudo("service nginx restart")

