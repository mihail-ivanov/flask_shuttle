
import sys
import os

import logging
import io
from logging import StreamHandler, DEBUG
from os.path import dirname, abspath
from tempfile import mkstemp
from docopt import docopt
import shutil
import errno
import random


logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


def _secret_key():
    random_generator = random.SystemRandom()
    length = 50
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)'
    return ''.join(random_generator.choice(chars) for i in range(length))


def _project_parameters(project_name):
    return {
        'project_name': project_name,
        'csrf_session_key': _secret_key(),
        'secret_key': _secret_key(),
    }


def generate_project(args):
    # Project templates
    project_source = os.path.join(dirname(abspath(__file__)), 'templates', 'project')

    # Get the name of the project
    project_name = args.get('<project>')

    if not project_name:
        logger.warning('Project name cannot be empty.')
        return

    project_parameters = _project_parameters(project_name)

    # Destination project path
    project_dir = os.path.join(os.getcwd(), project_name)

    if os.path.isdir(project_dir):
        logger.warning('Project directory already exists.')
        return

    logger.info('Creating project {project_name} ...'.format(project_name))

    _mkdir_p(project_dir)

    for src_dir, sub_dirs, filenames in os.walk(project_source):
        # Build and create destination directory path
        relative_path = src_dir.split(src)[1].lstrip(os.path.sep)
        dst_dir = os.path.join(dst, relative_path)

        if src != src_dir:
            _mkdir_p(dst_dir)

        # Copy, rewrite and move project files
        for filename in filenames:
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)

            if filename.endswith(REWRITE_FILE_EXTS):
                _rewrite_and_copy(src_file, dst_file, project_name)
            else:
                shutil.copy(src_file, dst_file)

            logger.info("New: %s" % dst_file)

    logger.info('Project created succesfully.')


def main():
    if args.get('new'):
        generate_project(args)
    else:
        print(args)


def _mkdir_p(path):
    try:
        os.makedirs(path)
    else:
        logger.info("New: %s%s", path, os.path.sep)


def _rewrite_and_copy(src_file, dst_file, project_name):
    """Replace vars and copy."""
    # Create temp file
    fh, abs_path = mkstemp()

    with io.open(abs_path, 'w', encoding='utf-8') as new_file:
        with io.open(src_file, 'r', encoding='utf-8') as old_file:
            for line in old_file:
                new_line = line.replace('#{project}', project_name). \
                    replace('#{project|title}', project_name.title())
                new_file.write(new_line)

    # Copy to new file
    shutil.copy(abs_path, dst_file)
    os.close(fh)


if __name__ == "__main__":
    main()
