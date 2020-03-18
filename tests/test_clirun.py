#!/usr/bin/env python3
import unittest
from click.testing import CliRunner
from scripts.init import cli

class TestCliRunOkay(unittest.TestCase):
    def test_cli_help_execute(self):
        """Test that cli can actually execute"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert 'Usage:' in result.output

if __name__ == '__main__':
    unittest.main()
