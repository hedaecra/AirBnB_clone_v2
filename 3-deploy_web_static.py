#!/usr/bin/python3
""" Creates and distributes an archive to your web servers """
from os.path import exists
from datetime import datetime
from fabric.api import local, env, put, run

env.hosts = ['35.196.102.248', '34.148.155.116']


def do_pack():
    """ Function that generates tgz archive """
    if not exists("versions"):
        local("mkdir versions")
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        name_archive = "versions/web_static_{}.tgz".format(date)
        local('tar -cvzf {} web_static'.format(name_archive))
        return name_archive
    except Exception as e:
        return None


def do_deploy(archive_path):
    """ Distributes"""
    if not exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]
        path = "/data/web_static/releases/{}".format(name)
        put(archive_path, '/tmp/')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}/'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path))
        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """ Distributes an archive to your web servers """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
