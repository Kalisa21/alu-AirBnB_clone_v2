#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers
"""

from fabric.api import env, run, put
from os.path import exists
from datetime import datetime

env.hosts = ['54.174.30.113', '3.95.216.87']
env.user = 'ubuntu'  # Replace with your SSH username

def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<filename without extension>
        filename = archive_path.split('/')[-1]
        folder_name = filename.split('.')[0]
        path_without_extension = '/data/web_static/releases/{}'.format(folder_name)

        run('mkdir -p {}'.format(path_without_extension))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_without_extension))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -f /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(path_without_extension))

        print('New version deployed!')
        return True

    except Exception as e:
        print('Deployment failed: {}'.format(e))
        return False

