# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

import builtins
import datapackage
import json
import responses
from mock import patch, mock_open, MagicMock

from dpm.main import cli
from .base import BaseCliTestCase, StringIO


class ReadmeTest(BaseCliTestCase):
    """
    Testcase for the Readme information.
    """

    def setUp(self):
        # GIVEN datapackage that can be treated as valid by the dpm
        self.valid_dp = datapackage.DataPackage({
            "name": "some-datapackage",
            "resources": [
                {"name": "some-resource", "path": "./data/some_data.csv", }
            ]
        })
        patch('dpm.main.datapackage', DataPackage=lambda *a: self.valid_dp).start()
        patch('dpm.main.exists', lambda *a: True).start()
        patch('dpm.main.open', lambda *a: StringIO('{}')).start()

        # AND the registry server that accepts any user
        responses.add(
            responses.POST, 'https://example.com/api/auth/token',
            json={'token': 'blabla'},
            status=200)


    @unittest.skip("TODO: logging")
    @patch('dpm.dpmclient.filter', lambda a, b: ['README.md'])
    def test_readme_sucess_with_extension(self):
        # WHEN `dpm publish` is invoked
        result = self.invoke(cli, ['publish'])

        # Checking README
        self.assertNotIn('Publishing Package without README', result.output)

    @unittest.skip("TODO: logging")
    @patch('dpm.dpmclient.filter', lambda a, b: ['README'])
    def test_readme_sucess_without_extension(self):
        # WHEN `dpm publish` is invoked
        result = self.invoke(cli, ['publish'])

        # Checking README
        self.assertNotIn('Publishing Package without README', result.output)

    @unittest.skip("TODO: logging")
    @patch('dpm.dpmclient.filter', lambda a, b: ['README.'])
    def test_readme_warning_invalid_extension(self):
        # WHEN `dpm publish` is invoked
        result = self.invoke(cli, ['publish'])

        # Checking README
        self.assertIn('Publishing Package without README', result.output)

    @unittest.skip("TODO: logging")
    @patch('dpm.dpmclient.filter', lambda a, b: [])
    def test_readme_warning_for_noreadme(self):
        # WHEN `dpm publish` is invoked
        result = self.invoke(cli, ['publish'])

        # Checking README
        self.assertIn('Publishing Package without README', result.output)

    @patch('dpm.dpmclient.filter',
           lambda a, b: ['README.', 'README.txt', 'README.md', 'README'])
    @patch('dpm.utils.file.open', mock_open())  # mock csv file open
    @patch('dpm.utils.file.getsize', lambda a: 5)  # mock csv file size
    @patch('dpm.dpmclient.md5_file_chunk', lambda a:
           '855f938d67b52b5a7eb124320a21a139')  # mock md5 checksum
    def test_readme_sucess_for_multiple_readme(self):
        # GIVEN the registry server accepts any datapackage
        responses.add(
            responses.PUT, 'https://example.com/api/package/user/some-datapackage',
            json={'message': 'OK'},
            status=200)
        # AND registry server gives bitstore upload url
        responses.add(
            responses.POST, 'https://example.com/api/auth/bitstore_upload',
            json={'key': 'https://s3.fake/put_here'},
            status=200)
        # AND s3 server allows data upload
        responses.add(
            responses.PUT, 'https://s3.fake/put_here',
            json={'message': 'OK'},
            status=200)
        # AND registry server successfully finalizes upload
        responses.add(
            responses.POST, 'https://example.com/api/package/user/some-datapackage/finalize',
            json={'message': 'OK'},
            status=200)
        # WHEN `dpm publish` is invoked
        result = self.invoke(cli, ['publish'])
        self.assertRegexpMatches(result.output, 'publish ok')

        # TODO: logging
        # Checking README uploading first match
        #self.assertNotIn('Publishing Package without README', result.output)
        #self.assertIn('Uploading README.txt', result.output)
