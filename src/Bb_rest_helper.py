import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import time

import datetime

import jwt
import requests
from requests import HTTPError

logger = logging.getLogger('Bb_rest_helper')
logger.propagate = False

# Get_Config
# A convience class to get configuration values that we do not want to show
# (or upload to github) (key, secret, url) from a json file.It also sets up
# logging for the helper classes. If logging is not set up, will just print
# to the console.
# Template format is simple
# {
#   "url":"",
#   "key":"",
#   "secret":""
# }


class Get_Config():

    logger = logging.getLogger('Bb_rest_helper')
    logger.propagate = False

    # Initializes the class by taking the configuration file path
    # as an argument, a typical value would be "./config.json".
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            with open(self.file_path) as conf:
                self.data = json.load(conf)
                logger.info("Configuration file loaded")
        except FileNotFoundError as e:
            logger.error('No configuration file found - Exit program')
            sys.exit()

    # Returns url value from the configuration file to a variable
    def get_url(self):
        return self.data["url"]

    # Returns key value from the configuration file to a variable
    def get_key(self):
        return self.data["key"]

    # Returns secret value from the configuration file to a variable
    def get_secret(self):
        return self.data["secret"]

    # (ALLY ONLY) Returns client_id from the configuration file to a variable
    def get_client_id(self):
        return self.data["client_id"]

# Auth_Helper
# A class to simplify REST API authentication for the Blackboard API.


class Auth_Helper():

    logger = logging.getLogger('Bb_rest_helper')
    logger.propagate = False

    # Initializes the auth helper by taking the target system url,
    # PI key and secret as arguments.
    def __init__(self, url: str, key: str, secret: str):
        self.url = url
        self.key = key
        self.secret = secret
        self.learn_token = None
    
    # Method that returns True when the token expires. Used by the learn_auth() method.
    def token_is_expired(self, expiration_datetime):
        self.expiration_datetime = expiration_datetime
        self.time_left = (self.expiration_datetime -
                          datetime.datetime.now()).total_seconds()
        if self.time_left < 1:
            time.sleep(1)
            return True
        else:
            return False

    # Returns the authentication token for Blackboard Learn.
    def learn_auth(self):
        self.endpoint = "/learn/api/public/v1/oauth2/token"
        self.params = {"grant_type": "client_credentials"}
        self.headers = {
            'Content-Type': "application/x-www-form-urlencoded"}

        try:
            if self.learn_token == None:

                r = requests.request(
                    "POST",
                    self.url +
                    self.endpoint,
                    headers=self.headers,
                    params=self.params,
                    auth=(
                        self.key,
                        self.secret))
                r.raise_for_status()
                self.data = json.loads(r.text)
                self.learn_token = self.data["access_token"]
                self.expires = self.data["expires_in"]
                m, s = divmod(self.expires, 60)
                self.now = datetime.datetime.now()
                self.expires_at = self.now + \
                    datetime.timedelta(seconds=s, minutes=m)
                logger.info("Learn Authentication successful")
                logger.info("Token expires at: " + str(self.expires_at))
                return self.learn_token
                
            elif self.token_is_expired(self.expires_at):
                logger.info('refresh token')
                r = requests.request(
                    "POST",
                    self.url +
                    self.endpoint,
                    headers=self.headers,
                    params=self.params,
                    auth=(
                        self.conf.get_key(),
                        self.conf.get_secret()))
                r.raise_for_status()
                self.data = json.loads(r.text)
                self.learn_token = self.data["access_token"]
                self.expires = self.data["expires_in"]
                m, s = divmod(self.expires, 60)
                self.now = datetime.datetime.now()
                self.expires_at = self.now + \
                    datetime.timedelta(seconds=s, minutes=m)
                logger.info("Learn Authentication successful")
                logger.info("Token expires at: " + str(self.expires_at))
                return self.learn_token

        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["error_description"])



# A separate class to support Ally as a service requests.
# it is separated as it uses different authentication and has
# a still limited set of features


class Ally_Helper():

    logger = logging.getLogger('Bb_rest_helper')
    logger.propagate = False

    # Initializes the auth helper by taking the target system url,
    # PI key and secret as arguments.
    def __init__(self, url: str, client_id: str, key: str, secret: str):
        self.url = url
        self.client_id = client_id
        self.key = key
        self.secret = secret

    # Returns the authentication token for Blackboard Ally. Ally does not use
    # a post call to an endpoint, instead, it encodes a jwt assertion that then
    # is passed as a Bearer token.
    def ally_auth(self):
        self.iat = str(int(time.time()))
        self.headers = {
            'typ': 'JWT',
            'alg': "Rs256"
        }
        self.claims = {
            "clientId": self.client_id,
            "iat": self.iat
        }
        self.assertion = jwt.encode(self.claims, self.secret).decode("utf-8")
        self.ally_token = str(self.assertion)
        return self.ally_token

    # Uploads a file to ally service, getting the path to the file and the auth header
    # arguments
    def ally_upload_file(self, token: str, file_path: str):
        self.file_path = file_path
        self.token = token
        self.headers = {
            "Authorization": f'Bearer {self.token}'
        }
        self.ally_url = f'{self.url}/api/v2/clients/{self.client_id}/content'
        self.files = {
            'file': open(file_path, 'rb')
        }
        try:
            r = requests.request(
                'POST',
                self.ally_url,
                files=self.files,
                headers=self.headers)
            r.raise_for_status()
            data = json.loads(r.text)
            logger.info(
                'File uploaded to Ally, check processing status via ally_check_status()')
            return data
        except requests.exceptions.HTTPError as e:
            logger.warning('An error occured during the request')

    # Returns the file hash to be used in the next requests from the upload
    # request response
    def ally_get_hash(self, upload_response: dict):
        self.upload_response = upload_response
        logger.info('Hash value extracted to a variable')
        return self.upload_response["hash"]

    # Checks the status of a file upload to Ally as a service, takes toekn and content hash
    # as arguments.
    def ally_check_status(self, token: str, content_hash: str):
        self.content_hash = content_hash
        self.token = token
        self.headers = {
            "Authorization": f'Bearer {self.token}'
        }
        self.check_url = f'{self.url}/api/v2/clients/{self.client_id}/content/{content_hash}/status'
        try:
            r = requests.request('GET', self.check_url, headers=self.headers)
            r.raise_for_status()
            data = json.loads(r.text)
            logger.info('status checked. See response for details')
            return data
        except requests.exceptions.HTTPError as e:
            logger.warning('An error occured during the request')

    def ally_get_feedback(
            self,
            token: str,
            content_hash: str,
            feedback: bool = True):
        self.content_hash = content_hash
        self.token = token
        self.feedback = feedback
        self.feedback_url = f'{self.url}/api/v2/clients/{self.client_id}/content/{content_hash}'
        self.headers = {
            "Authorization": f'Bearer {self.token}'
        }
        self.params = {
            "feedback": self.feedback
        }
        try:
            r = requests.request(
                'GET',
                self.feedback_url,
                headers=self.headers,
                params=self.params)
            r.raise_for_status()
            data = json.loads(r.text)
            logger.info('Feedback obtained, see response for details')
            return data
        except requests.exceptions.HTTPError as e:
            logger.error('An error occured during the request', exc_info=True)

# Bb_Requests
# A class to simplify API calls to Blackboard REST APIs, provides functions
# for GET, POST, PUT, PATCH and DELETE


class Bb_Requests():

    logger = logging.getLogger('Bb_rest_helper')
    logger.propagate = False

    # GET request. It takes a GET endpoint from the API, the authentication
    # token and a list of parameters as arguments. This request has been updated
    # to support pagination. Note this is currently a heavy method, use parameters
    # limit responses if needed.

    def Bb_GET(
            self,
            base_url: str,
            endpoint: str,
            token: str,
            params: dict = {}):
        self.base_url = base_url
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.request_url = f'{self.base_url}{self.endpoint}'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        data_from_pages = []
        try:

            r = requests.request('GET', self.request_url,
                                 headers=self.headers, params=self.params)

            data = json.loads(r.text)
            r.raise_for_status()

            for d in data['results']:
                data_from_pages.append(d)

            while data['paging']['nextPage']:
                self.offset_url = f'{self.base_url}{data["paging"]["nextPage"]}'
                r = requests.get(
                    self.offset_url, headers={
                        f'Authorization': f'Bearer {self.token}'})
                data = json.loads(r.text)
                for d in data['results']:
                    data_from_pages.append(d)

        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])

        except BaseException:
            # returns data from Learn REST API, all pages
            logger.info("GET Request completed")
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            return data_from_pages


    # POST request. It takes a POST endpoint from the API, the authentication token,
    # a list of parameters, and a json payload as arguments.

    def Bb_POST(
            self,
            base_url: str,
            endpoint: str,
            token: str,
            payload: dict,
            params: dict = {}):
        self.base_url = base_url
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.request_url = f'{self.base_url}{self.endpoint}'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request(
                'POST',
                self.request_url,
                headers=self.headers,
                params=self.params,
                json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            logger.info("POST Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])


    # Uploads a file to the Blacboard Learn Api uploads endpoint, getting the path to the file and the auth header
    # arguments, it returns the file id that will be used in other calls to
    # the API (i.e. Creating content)
    def Bb_POST_file(self, base_url: str, token: str, file_path: str):
        self.base_url = base_url
        self.file_path = file_path
        self.token = token
        self.headers = {
            "Authorization": f'Bearer {self.token}'
        }
        self.uploads_url = f'{self.base_url}/learn/api/public/v1/uploads'
        self.files = {
            'file': open(file_path, 'rb')
        }
        try:
            r = requests.request(
                'POST',
                self.uploads_url,
                files=self.files,
                headers=self.headers)
            r.raise_for_status()
            data = json.loads(r.text)
            logger.info(
                'File uploaded to temporary storage, returning id')
            logger.info("GET Request completed")
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            return data['id']
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])

    # PATCH request. It takes a PATCH endpoint from the API, the authentication token,
    # a list of parameters, and a json payload as arguments. A PATCH requests allows
    # to update a record partially.

    def Bb_PATCH(
            self,
            base_url: str,
            endpoint: str,
            token: str,
            payload: dict,
            params: dict = {}):
        self.base_url = base_url
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.request_url = f'{self.base_url}{self.endpoint}'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request(
                'PATCH',
                self.request_url,
                headers=self.headers,
                params=self.params,
                json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            logger.info("PATCH Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])

    # PUT request. It takes a PUT endpoint from the API, the authentication token,
    # a list of parameters, and a json payload as arguments. A PUT request is meant
    # to update a record entirely.
    def Bb_PUT(
            self,
            base_url: str,
            endpoint: str,
            token: str,
            payload: dict,
            params: dict = {}):
        self.base_url = base_url
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.request_url = f'{self.base_url}{self.endpoint}'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request(
                'PUT',
                self.request_url,
                headers=self.headers,
                params=self.params,
                json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            logger.info("PUT Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])

    # DELETE request. It takes a DELETE endpoint from the API, the authentication token
    # and a list of parameters as arguments.
    def Bb_DELETE(
            self,
            base_url: str,
            endpoint: str,
            token: str,
            params: dict = {}):
        self.base_url = base_url
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.request_url = f'{self.base_url}{self.endpoint}'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request(
                'DELETE',
                self.request_url,
                headers=self.headers,
                params=self.params)
            # A successful DELETE request returns a 204 code meaning that the server has
            # fulfilled the request but that there is no content to return.
            r.raise_for_status()
            logger.info(f'API limit: {r.headers["X-Rate-Limit-Limit"]}')
            logger.info(
                f'Remaining API calls: {r.headers["X-Rate-Limit-Remaining"]}')
            logger.info(
                f'Time to reset API limit: {r.headers["X-Rate-Limit-reset"]}')
            logger.info("DELETE Request completed")
        except KeyError:
            # Collaborate does not provide rate limit information, so just
            # logging the request status and returning the data
            logger.info("DELETE Request completed")
        except requests.exceptions.HTTPError as e:
            logger.error('The resource could not be deleted')

# A set of convenience functions (logging, printing, checking courses...),
# this will be extended over time.


class Bb_Utils():

    logger = logging.getLogger('Bb_rest_helper')
    logger.propagate = False

    # Sets logging with default path to ./logs and default level of DEBUG.
    def set_logging(self, path: str = './logs', level=logging.DEBUG, when='h', interval=1):
        self.path = path
        self.level = level
        self.when = when
        self.interval = interval
        try:
            os.mkdir(self.path, 0o777)
            logger = logging.getLogger('Bb_rest_helper')
            logger.propagate = False
            logger.setLevel(self.level)
            handler = TimedRotatingFileHandler(f'{self.path}/Bb_rest_helper_log',
                                               when=self.when,
                                               interval=self.interval,
                                               backupCount=5)
            formatter = logging.Formatter(
                '%(asctime)-15s %(name)-22s %(funcName)-15s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.info('Logs folder created')
            logger.info('Logging has been set up')
        except FileExistsError:
            logger = logging.getLogger('Bb_rest_helper')
            logger.propagate = False
            logger.setLevel(self.level)
            handler = TimedRotatingFileHandler(f'{self.path}/Bb_rest_helper_log',
                                               when=self.when,
                                               interval=self.interval,
                                               backupCount=5)
            formatter = logging.Formatter(
                '%(asctime)-15s %(name)-22s %(funcName)-15s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.info('Logging has been set up')

    # Prints the response from any of the above methods in a prettified format
    # to the console.
    def pretty_printer(self, data: dict, sort_keys: bool = True):
        self.data = data
        self.sort_keys = sort_keys
        if data:
            print(json.dumps(self.data, indent=4, sort_keys=self.sort_keys))
            logger.info("Results printed to the console.")
        else:
            logger.warning("No data to print.")

    # Checks if a given Learn course exists in the server
    def check_course_id(self, token: str, external_course_id: str):
        self.token = token
        self.external_course_id = external_course_id
        try:
            endpoint_courses = "/learn/api/public/v3/courses"
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': "Application/json"
            }
            params = {
                "externalId": self.external_course_id,
                "fields": "id"
            }
            r = requests.request(
                'GET',
                f'{self.url}{endpoint_courses}',
                headers=headers,
                params=params)
            r.raise_for_status()
            data = json.loads(r.text)
            if data["results"]:
                logger.info('The course has been found in the server.')
                return True
            else:
                logger.warning(
                    'The course could not be found, please check that the provided course id is the external id')
                return False
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])

    # This method is provided to facilitate date formatting when importing dates from
    # other applications, i.e, dates in excel format, it can take a date string with
    # the following formats
    # DD/MM/YYYY
    # DD/MM/YYYY HH:MM
    # DD/MM/YYYY HH:MM:SS
    # optional arguments for date delimiter (default "/") and hour delimiter (default ":")
    # can be provided. The outcome of the method is YYYY-MM-DDTHH:MM:SS:000Z
    def time_format(
            self,
            dt: str,
            date_delimiter: str = "/",
            hour_delimiter: str = ":"):
        self.dt = dt
        self.date_delimiter = date_delimiter
        self.hour_delimiter = hour_delimiter
        if len(self.dt) < 11:
            split_date = dt.split(self.date_delimiter)
            date_formatted = datetime.datetime(int(split_date[2]), int(split_date[1]), int(
                split_date[0])).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return date_formatted
        elif len(self.dt) > 11 and len(self.dt) < 17:
            split_date = self.dt.split(self.date_delimiter)
            split_year = split_date[2].split()
            split_hour = split_year[1].split(self.hour_delimiter)
            date_formatted = datetime.datetime(int(split_year[0]), int(split_date[1]), int(split_date[0]), int(
                split_hour[0]), int(split_hour[1])).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return date_formatted
        else:
            split_date = self.dt.split(self.date_delimiter)
            split_year = split_date[2].split()
            split_hour = split_year[1].split(self.hour_delimiter)
            date_formatted = datetime.datetime(int(split_year[0]), int(split_date[1]), int(split_date[0]), int(
                split_hour[0]), int(split_hour[1]), int(split_hour[2])).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return date_formatted

    # This method is used to get the external id of a learn course as an argument and return
    # another field in the get response (usually the course id). We found it is a common operation,
    # particularly when getting a list of
    # courses in a CSV
    def learn_convert_external_id(
            self,
            url: str,
            token: str,
            external_id: str,
            final_id: str = "id"):
        self.url = url
        self.token = token
        self.external_id = external_id
        self.final_id = final_id
        self.url_courses = f'{self.url}/learn/api/public/v3/courses'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        params = {
            "externalId": self.external_id,
            "fields": self.final_id
        }
        try:
            r = requests.request(
                'GET', self.url_courses, headers=headers, params=params)
            r.raise_for_status()
            data = json.loads(r.text)
            if len(data) == 1:
                logger.info("Course externalId converted to course Id")
                return data["results"][0][self.final_id]
            else:
                logger.warning(
                    "Several results have been found, please use a more specific Id")
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logger.error(data["message"])


# A convenience method that further abstracts the setup and authentication process to return the token and the url in
# just one line. This method is just for Learn and collaborate. The url has been added to avoid having to hardcode
# this value or having to call Get_Config separately.

    def quick_auth(self, filepath: str, platform: str='Learn'):
        self.filepath = filepath
        self.platform = platform
        self.conf = Get_Config(self.filepath)
        self.url = self.conf.get_url()
        self.key = self.conf.get_key()
        self.secret = self.conf.get_secret()
        self.auth = Auth_Helper(self.url, self.key, self.secret)
        if self.platform == "Learn":
            self.token = self.auth.learn_auth()
            data = {
                'token': self.token,
                'url': self.url
            }
            return data
        else:
            logger.error(
                'Collaborate methods have been removed from V3. "platform" argument ketp for compatibility with default value of "Learn"')
