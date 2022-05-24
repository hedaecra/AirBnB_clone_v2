#!/usr/bin/python3
""" Module python called 2-do_deploy_web_static.py """
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists

env.user = 'ubuntu'
env.hosts = [
    '52.55.249.213',
    '54.157.32.137'
]


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder """
    # Create folder versions and format datatime
    new_folder = local("mkdir -p versions")
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    format_file_tar = "versions/web_static_" + date_time + ".tgz"
    # make a compressed TAR file
    file_tar = local("tar -czvf {} web_static".format(format_file_tar))
    if file_tar.failed:
        return None
    else:
        return "{}".format(format_file_tar)


def do_deploy(archive_path):
    """ Fabric script (based on the file 1-pack_web_static.py) that
        distributes an archive to your web servers.
        Returns True if all operations have been done correctly,
        otherwise returns False
    """
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
