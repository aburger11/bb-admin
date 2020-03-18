#!/usr/bin/env python3

import unittest
import lib.create as c
from unittest.mock import patch
from unittest import mock
from lib.base import BitBucketAdmin

# Mock requests as a whole
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
        def raise_for_status(self):
            pass
    # If we're looking for a user's permissions, deny it (foo instead of admin)
    if '/user/permissions/teams' in args[0]:
        return MockResponse({'values':[{'permission':'foo'}]}, 200)
    else:
        return MockResponse({}, 200)

class TestsNotOkay(unittest.TestCase):
    # Mocked requests from above
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @patch.object(c.CreateRepo,'_convert_usernames')
    def test_reject_nonadmin(self, mockedget, mockconvert):
        """Test that non-admins get sys.exit()ed"""
        with self.assertRaises(SystemExit) as sysexittest:
            testobj = c.CreateRepo(
                login='user', passwd='password', project='do', repo='test-repo'
            )

class TestsOkay(unittest.TestCase):
    @patch.object(c.BitBucketAdmin,'_verify_auth')
    @patch.object(c.BitBucketAdmin,'_verify_admin')
    @patch.object(c.CreateRepo,'_convert_usernames')
    def test_create_obj(self, mockadmin, mockauth, mockconvert):
        """Test that created object is a CreateRepo, a subclass of BitBucketAdmin"""
        # Stub out admin & auth calls so we can actually create an object
        mockadmin.return_value = True
        mockauth.return_value = True
        testobj = c.CreateRepo(
            login='user', passwd='password', project='do', repo='test-repo'
        )
        self.assertIsInstance(testobj,c.CreateRepo)     # Subclass
        self.assertIsInstance(testobj,BitBucketAdmin)   # Superclass

if __name__ == '__main__':
    unittest.main()
