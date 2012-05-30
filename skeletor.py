#!/usr/bin/env python

import argparse
import errno
import logging
import os
import re

import jinja2


log = logging.getLogger(__name__)


class CommandError(Exception):
    pass


def validate_module_name(name):
    if not re.search(r'^[_A-Za-z][_A-Za-z0-9]*$', name):
        if not re.search(r'^[_A-Za-z]', name):
            message = 'make sure that the name starts with a letter or an underscore'
        else:
            message = 'use only letters, numbers and underscores'
        raise CommandError(
            '%r is not a valid project name. Please %s.' % (name, message)
        )
    return name


def mkdir(name):
    try:
        os.mkdir(name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def skeletor():
    parser = argparse.ArgumentParser(
        description='Copy a project layout template into the specified directory.'
    )

    parser.add_argument('name', help='The name of the project.')
    parser.add_argument('-t', '--template',
        required=True,
        help='Path to the template directory.'
    )
    parser.add_argument('-d', '--directory',
        help='The directory where the template should be copied into. '
             'Defaults to the current working directory.'
    )
    parser.add_argument('-e', '--extension',
        action='append', dest='extensions', metavar='EXT', default=[],
        help='The file extension(s) to render. '
             'You may provide multiple extensions by using -e multiple times.'
    )
    parser.add_argument('-f', '--filename', dest='files',
        action='append', default=[],
        help='The file name(s) to render. '
             'You may provide multiple file names by using -e multiple times.'
    )
    parser.add_argument('-v', '--verbose',
        action='store_true', default=False,
        help='Verbose output.'
    )

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.INFO)

    # Make sure that the project name is a valid Python module name.
    project_name = validate_module_name(args.name)

    extensions = tuple(args.extensions)

    if args.directory is None:
        # If target directory is not given, create a new directory named after
        # the project name to the current working directory.
        directory = os.path.join(os.getcwd(), project_name)
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno == errno.EEXIST:
                message = "'%s' already exists" % directory
            else:
                message = e
            raise CommandError(message)
    else:
        directory = os.path.abspath(os.path.expanduser(args.directory))
        if not os.path.exists(directory):
            raise CommandError("Target directory '%s' does not exist. "
                               "Please create it first." % directory)

    context = {'project_name': project_name}

    template_dir = os.path.abspath(os.path.expanduser(args.template))
    if not os.path.exists(template_dir):
        raise CommandError("Could not find template directory "
                           "'%s'" % template_dir)

    prefix_length = len(template_dir) + 1

    for root, dirs, files in os.walk(template_dir):
        relative_dir = root[prefix_length:]
        relative_dir = relative_dir.replace('project_name', project_name)

        if relative_dir:
            mkdir(os.path.join(directory, relative_dir))

        # Skip hidden directories
        for dirname in dirs[:]:
            if dirname.startswith('.'):
                dirs.remove(dirname)

        for filename in files:

            if filename.endswith(('.pyc',)):
                continue

            old_path = os.path.join(root, filename)
            new_path = os.path.join(directory, relative_dir,
                filename.replace('project_name', project_name))

            if os.path.exists(new_path):
                raise CommandError('%s already exists.' % new_path)

            log.info('Creating %s', new_path)

            with open(old_path, 'r') as template_file:
                content = template_file.read()
                newline = content.endswith('\n')

            if filename.endswith(extensions) or filename in args.files:
                template = jinja2.Template(content)
                content = template.render(**context)
                if newline:
                    content += '\n'

            with open(new_path, 'w') as new_file:
                new_file.write(content)


if __name__ == '__main__':
    skeletor()
