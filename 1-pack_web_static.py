#!/usr/bin/python3
""" Module python called 1-pack_web_static """
from fabric.api import local
from datetime import datetime


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
