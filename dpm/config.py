# -*- coding: utf-8 -*-
"""
Configuration file reading/writing utils and defaults.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from os.path import exists, join
from builtins import input

from configobj import ConfigObj
from getpass import getpass
from .utils.compat import expanduser
from .utils.click import echo


configdir = expanduser('~/.dpm')
if not exists(configdir):
    os.makedirs(configdir)

# The config file in INI(ConfigObj) format.
configfile = join(configdir, 'config')


# TODO: should we have hardcoded server default? Or always require user to enter?
DEFAULT_SERVER = 'https://example.com'


def prompt_config(config_path):
    """
    Ask user to enter config variables and then save it to disk.
    """
    config = ConfigObj(config_path)

    echo('Please enter your username to authenticate '
        'for the datapackage registry server.')
    while True:
        config['username'] = input('Username: ')
        if config['username']:
            break
        else:
            echo('\nUsername should not be empty.')

    echo('\nPlease enter your password to authenticate '
          'for the datapackage registry server.')
    while True:
        config['password'] = getpass('Your password (input hidden): ')
        if config['password']:
            break
        else:
            echo('\nPassword should not be empty.')

    echo('\nPlease enter registry server url. '
          'Leave blank to use default value: %s' % DEFAULT_SERVER)
    config['server'] = input('Server URL: ')

    config.write()
    echo('Configuration saved')


def read_config(config_path):
    """
    Read configuration from file, falling back to env or hardcoded defaults.
    """
    config = ConfigObj(config_path)
    return  {
        'server': os.environ.get('DPM_SERVER') \
                  or config.get('server') \
                  or DEFAULT_SERVER,
        'username': os.environ.get('DPM_USERNAME') or config.get('username'),
        'password': os.environ.get('DPM_PASSWORD') or config.get('password')
    }
