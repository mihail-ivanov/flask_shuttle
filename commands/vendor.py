
import os
import shutil
from git import Repo
from urllib.request import urlretrieve

from flask import current_app
from flask_script import Command
from flask_script import Manager


class VendorDownload(Command):
    """Download vendor libraries"""

    def _delete_path(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

    def _git_download(self, location, vendor_path):
        print('- assets: downloading ' + location)
        repo_name = location.rsplit('/', 1)[-1]
        destination_path = os.path.join(vendor_path, repo_name)
        self._delete_path(destination_path)
        Repo.clone_from(location, destination_path)

    def _file_download(self, location, vendor_path):
        print('- assets: downloading ' + location)
        file_name = location.rsplit('/', 1)[-1]
        file_path = os.path.join(vendor_path, file_name)
        self._delete_path(file_path)
        urlretrieve(location, file_path)

    def run(self):
        """
        Downloads the configured assets
        """

        from app.assets import ASSET_RESOURCES

        vendor_path = os.path.join(current_app.config['BASE_DIR'], 'app', 'assets', 'vendor')

        for resource in ASSET_RESOURCES:
            if resource['type'] == 'git':
                self._git_download(resource['location'], vendor_path)
            elif resource['type'] == 'file':
                self._file_download(resource['location'], vendor_path)


VendorManager = Manager(usage='Manages vendor libraries')
VendorManager.add_command('download', VendorDownload())
