# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import datapackage
import responses
from mock import patch

from dpm.main import cli
from .base import BaseCliTestCase


class ConfigureSuccessTest(BaseCliTestCase):
    """
    When user launches `dpmpy configure` and provides valid values for inputs,
    configuration should be saved to disk.
    """

    def test_configure_success(self):
        # GIVEN valid inputs for options
        options = {
            'Username: ': 'user',
            'Your password: ': 'password',
            'Server URL: ': 'http://example.com'
        }
        patch('dpm.client.do_configure.input', lambda opt: options[opt]).start()
        patch('dpm.client.do_configure.getpass', lambda opt: options[opt]).start()

        # WHEN `dpm configure` is invoked
        result = self.invoke(cli, ['configure'])

        # THEN config should be written to disk
        self.config.write.assert_called_once()
        # AND exit code should be 0
        self.assertEqual(result.exit_code, 0)
