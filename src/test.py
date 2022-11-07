import datetime
import glob
import logging
import os
import os.path
import shutil
import time
import unittest

import vcr

from Bb_rest_helper import Auth_Helper, Bb_Requests, Bb_Utils, Get_Config


class Tests_Bb_rest_helper(unittest.TestCase):

    # runs before each test, sets up logging and authentication
    # @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_setup')
    def setUp(self):
        self.utils = Bb_Utils()
        self.utils.set_logging()
        self.quick_auth = self.utils.quick_auth(
            './Bb_rest_helper/credentials/config.json', 'Learn')
        self.learn_url = self.quick_auth['url']
        self.learn_token = self.quick_auth['token']

    # Runs after tests in the class, removes logs and log folder
    @classmethod
    def tearDownClass(Tests_Bb_rest_helper):
        shutil.rmtree('./logs')

    # Tests for Get_Config() class
    def test_get_url(self):
        config = Get_Config('./Bb_rest_helper/credentials/config.json')
        url = config.get_url()
        assert url

    def test_get_key(self):
        config = Get_Config('./Bb_rest_helper/credentials/config.json')
        key = config.get_key()
        assert key

    def test_get_secret(self):
        config = Get_Config('./Bb_rest_helper/credentials/config.json')
        secret = config.get_secret()
        assert secret

    def test_get_client_id(self):
        config = Get_Config('./Bb_rest_helper/credentials/ally_config.json')
        client_id = config.get_client_id()
        assert client_id

    # Tests for Auth_Helper() class
    def test_token_is_expired_true(self):
        self.config = Get_Config('./Bb_rest_helper/credentials/config.json')
        self.url = self.config.get_url()
        self.key = self.config.get_key()
        self.secret = self.config.get_secret()
        self.auth = Auth_Helper(self.learn_url, self.key, self.secret)
        # set expiration within one second to test FALSE
        self.now = datetime.datetime.now()
        self.expires_at = self.now + \
            datetime.timedelta(seconds=1)
        self.exp = self.auth.token_is_expired(self.expires_at)
        assert self.exp

    def test_token_is_expired_false(self):
        self.config = Get_Config('./Bb_rest_helper/credentials/config.json')
        self.url = self.config.get_url()
        self.key = self.config.get_key()
        self.secret = self.config.get_secret()
        self.auth = Auth_Helper(self.learn_url, self.key, self.secret)
        # set expiration within one second to test FALSE
        self.now = datetime.datetime.now()
        self.expires_at = self.now + \
            datetime.timedelta(seconds=5)
        self.exp = self.auth.token_is_expired(self.expires_at)
        self.assertFalse(self.exp)

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_learn_auth')
    def test_learn_auth(self):
        self.config = Get_Config('./Bb_rest_helper/credentials/config.json')
        self.url = self.config.get_url()
        self.key = self.config.get_key()
        self.secret = self.config.get_secret()
        self.auth = Auth_Helper(self.learn_url, self.key, self.secret)
        self.test_token = self.auth.learn_auth()
        assert self.test_token

    # Tests for Bb_Requests() class

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_GET')
    def test_Bb_GET(self):
        self.reqs = Bb_Requests()
        self.endpoint = '/learn/api/public/v1/announcements'
        self.params = {
            'limit': '1',
            'fields': 'id,title'
        }
        self.data = self.reqs.Bb_GET(
            self.learn_url, self.endpoint, self.learn_token, self.params)
        assert self.data[0]['id'], self.data[0]['title'] in self.data

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_POST')
    def test_Bb_POST(self):
        self.reqs = Bb_Requests()
        self.endpoint = '/learn/api/public/v1/announcements'
        self.params = {
            'fields': 'id,title'
        }
        self.payload = {
            "title": "Bb Rest helper test",
            "body": "<!-- {\"bbMLEditorVersion\":1} --><div data-bbid=\"bbml-editor-id_9c6a9556-80a5-496c-b10d-af2a9ab22d45\"> <h4>Header Large</h4>  <h5>Header Medium</h5>  <h6>Header Small</h6>  <p><strong>Bold&nbsp;</strong><em>Italic&nbsp;<span style=\"text-decoration: underline;\">Italic Underline</span></em></p> <ul>   <li><span style=\"text-decoration: underline;\"><em></em></span>Bullet 1</li>  <li>Bullet 2</li> </ul> <p>  <img src=\"@X@EmbeddedFile.requestUrlStub@X@bbcswebdav/xid-1217_1\">   <span>\"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\"</span> </p>  <p><span>&lt;braces test=\"values\" other=\"strange things\"&gt;</span></p> <p>Header Small</p> <ol>   <li>Number 1</li>   <li>Number 2</li> </ol>  <p>Just words followed by a formula</p>  <p><img align=\"middle\" alt=\"3 divided by 4 2 root of 7\" class=\"Wirisformula\" src=\"@X@EmbeddedFile.requestUrlStub@X@sessions/EA5F7FF3DF32D271D0E54AF0150D924A/anonymous/wiris/49728c9f5b4091622e2f4d183d857d35.png\" data-mathml=\"«math xmlns=¨http://www.w3.org/1998/Math/MathML¨»«mn»3«/mn»«mo»/«/mo»«mn»4«/mn»«mroot»«mn»7«/mn»«mn»2«/mn»«/mroot»«/math»\"></p> <p><a href=\"http://www.blackboard.com\">Blackboard</a></p> </div>",
            "availability": {
                "duration": {
                    "type": "Permanent",
                },
            },
            "showAtLogin": True,
            "showInCourses": False,
        }
        self.data = self.reqs.Bb_POST(
            self.learn_url, self.endpoint, self.learn_token, self.payload, self.params)
        assert self.data['id'], self.data['title'] in self.data

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_POST_file')
    def test_Bb_POST_file(self):
        self.reqs = Bb_Requests()
        self.file_path = './Bb_rest_helper/vcr_tests/test.docx'
        self.upload = self.reqs.Bb_POST_file(
            self.learn_url, self.learn_token, self.file_path)
        assert self.upload[0], 'Bb_Post_file was expected to return an id for the uploaded file'

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_PATCH')
    def test_Bb_PATCH(self):
        # Get the id for the assment to patch from the response
        self.announcement_id = '_1437_1'
        self.reqs = Bb_Requests()
        self.endpoint = f'/learn/api/public/v1/announcements/{self.announcement_id}'
        self.params = {
            'fields': 'id,title'
        }
        self.payload = {
            "title": "Bb Rest helper test modified",
            "body": "<p> This is the announcement text </p> ",
            "availability": {
                "duration": {
                    "type": "Permanent",
                },
            },
            "showAtLogin": True,
            "showInCourses": False
        }
        self.data = self.reqs.Bb_PATCH(
            self.learn_url, self.endpoint, self.learn_token, self.payload, self.params)
        assert self.data['id'], self.data['title'] in self.data

    @unittest.skip('Known issue, skipping until resolved in issue #87')
    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_PUT')
    def test_Bb_PUT(self):
        self.node_id = '_87_1'  # node from emeasedemo
        self.user_id = '_13016_1'  # user id from emeasedemo
        self.payload = {
            "nodeRoles": ["admin"]
        }
        self.reqs = Bb_Requests()
        self.endpoint = f'/learn/public/api/v1/institutionalHierarchy/nodes/{self.node_id}/admins/{self.user_id}'
        self.data = self.reqs.Bb_PUT(
            self.learn_url, self.endpoint, self.learn_token, self.payload)

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_Bb_DELETE')
    def test_Bb_DELETE(self):
        # Announcement id from emeasedemo, update if cassete changes.
        self.announcement_id = '_1437_1'
        self.reqs = Bb_Requests()
        self.endpoint = f'/learn/api/public/v1/announcements/{self.announcement_id}'
        self.data = self.reqs.Bb_DELETE(
            self.learn_url, self.endpoint, self.learn_token)

    # Tests for Bb_Utils() class
    def test_set_logging_folder(self):
        assert os.path.isdir('./logs')

    def test_set_logging_file(self):
        assert glob.glob('./logs/[Bb_helper_log_]*')
        time.sleep(2)

    @unittest.skip('Just a printer method')
    def test_pretty_printer(self):
        data = {'name': 'javier', 'surname': 'gregori', 'cat': 1}
        self.utils.pretty_printer(data)

    @unittest.skip('Skip for now, method needs updating, issue #79')
    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_check_course_id_true')
    def test_check_course_id_true(self):
        # External course id from Emeasedemo
        check = self.utils.check_course_id(
            self.learn_url, self.learn_token, 'AWPBL')
        assert check

    @unittest.skip('Skip for now, method needs updating, issue #79')
    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_check_course_id_false')
    def test_check_course_id_false(self):
        # Fake External course id to trigger False
        check = self.utils.check_course_id(
            self.learn_url, self.learn_token, '111111')
        self.assertFalse(check)

    def test_time_format_1(self, utils=Bb_Utils()):
        data = '02/02/2021'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T00:00:00.000Z')

    def test_time_format_2(self, utils=Bb_Utils()):
        data = '02/02/2021 23:45'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T23:45:00.000Z')

    def test_time_format_3(self, utils=Bb_Utils()):
        data = '02/02/2021 23:45:24'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T23:45:24.000Z')

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_learn_convert_external_id')
    def test_learn_convert_external_id(self):
        self.course_external_id = 'AWPBL'  # course external id from emeasedemo
        data = self.utils.learn_convert_external_id(
            self.learn_url, self.learn_token, self.course_external_id)
        assert data

    @vcr.use_cassette('./Bb_rest_helper/vcr_tests/test_quick_auth')
    def test_quick_auth(self):
        self.quick_auth = self.utils.quick_auth(
            './Bb_rest_helper/credentials/config.json', 'Learn')
        self.learn_url = self.quick_auth['url']
        self.learn_token = self.quick_auth['token']
        assert self.learn_url, self.learn_token


if __name__ == '__main__':
    unittest.main()
