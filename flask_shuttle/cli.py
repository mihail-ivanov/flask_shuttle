#!/usr/bin/env python
# coding: utf-8

"""
Flask Shuttle
Usage:
  shuttle new <project>
  shuttle -v | --version
  shuttle -h | --help
Options:
  -h, --help          Help information.
  -v, --version       Show version.
"""


import os
import logging
import random
import docopt
from logging import DEBUG
from logging import StreamHandler
from os.path import abspath
from os.path import dirname

from flask_shuttle import __version__


EXCLUDE_DIRS = [
    '__pycache__',
]


EXCLUDE_FILES = [
]


EXCLUDE_EXTENSIONS = [
    '.pyc',
]


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

    # Destination project path
    project_dir = os.path.join(os.getcwd(), project_name)

    if os.path.isdir(project_dir):
        logger.warning('Project directory already exists.')
        return

    logger.info('Creating project {} ...'.format(project_name))

    # Copy project template
    _copy_dir(project_source, project_dir, project_name)

    logger.info('Project created succesfully.')


def main():
    args = docopt.docopt(__doc__, version="Flask-Shuttle {0}".format(__version__))

    if args.get('new'):
        generate_project(args)
    else:
        print(args)


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except:
        raise
    else:
        logger.info("New: %s%s", path, os.path.sep)


def _copy_dir(from_dir, to_dir, project_name):
    project_parameters = _project_parameters(project_name)

    # Create destination directory
    if not os.path.exists(to_dir):
        _mkdir_p(to_dir)

    for src_dir, sub_dirs, filenames in os.walk(from_dir):
        # Skip directories from exclude list
        if os.path.basename(src_dir) in EXCLUDE_DIRS:
            continue

        # Build and create destination directory path
        relative_path = src_dir.replace('{}/'.format(from_dir), '')
        dest_dir = os.path.join(to_dir, relative_path)

        # Create project directory, if doesn't exists
        if not os.path.exists(dest_dir):
            _mkdir_p(dest_dir)

        # Copy, rewrite and move project files
        for filename in filenames:
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dest_dir, filename)

            # Skip files from exclude list
            if os.path.basename(src_file) in EXCLUDE_FILES:
                continue

            # Skip extensions from exclude list
            _, file_extension = os.path.splitext(src_file)
            if file_extension in EXCLUDE_EXTENSIONS:
                continue

            _copy_file(src_file, dst_file, project_parameters)
            logger.info("New: %s" % dst_file)


def _copy_file(src_file, dst_file, project_parameters):
    file_lines = []

    with open(src_file, 'r') as old_file:
        for line in old_file:
            new_line = line

            for param_name, param_value in project_parameters.items():
                new_line = new_line.replace('#{{{}}}'.format(param_name), param_value)

            file_lines.append(new_line)

    with open(dst_file, 'w') as new_file:
        for line in file_lines:
            new_file.write(line)


if __name__ == "__main__":
    main()
