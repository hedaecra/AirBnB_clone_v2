#!/usr/bin/python3
""" Module python called 2-deploy_web_static.py """
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import isfile

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
        distributes an archive to web servers.
        Returns True if all operations have been done correctly,
        otherwise returns False
    """
    if not isfile(archive_path):
        return False
    split_path = archive_path.split('/')[1]
    split_only_name = split_path.split('.')[0]
    # Uploading file
    file_up = put(archive_path, '/tmp/')
    if file_up.failed:
        return False
    # Create path where uncompress file
    path_create = run('mkdir -p /data/web_static/releases/{}'.format(
        split_only_name))
    if path_create.failed:
        return False
    # Uncompress the archive
    uncomp_file = run(
        'tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            split_path, split_only_name))
    if uncomp_file.failed:
        return False
    # Delete the file from the server
    delete_file = run('rm /tmp/{}'.format(split_path))
    if delete_file.failed:
        return False
    # Move the file to the rute create in path_create
    move_file = run(
        'mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
            split_only_name, split_only_name))
    if move_file.failed:
        return False
    # Delete the empty (now) directory
    delete_folder = run(
        'rm -rf /data/web_static/releases/{}/web_static'.format(
            split_only_name))
    if delete_folder.failed:
        return False
    # Delete symbolic link (current)
    delete_link = run('rm -rf /data/web_static/current')
    if delete_link.failed:
        return False
    # Create new symbolic link
    new_link = run(
        'ln -s /data/web_static/releases/{} /data/web_static/current'.format(
            split_only_name))
    if new_link.failed:
        return False

    return True


def deploy():
    """ Fabric script that creates and distributes an archive
        to web servers """
    _archive = do_pack()
    if _archive is None:
        return False
    distributate_archive = do_deploy(_archive)
    return distributate_archive
