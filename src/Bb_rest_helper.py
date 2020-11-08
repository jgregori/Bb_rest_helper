import json
import logging
import os
import sys
import time
from datetime import datetime

import jwt
import requests
from requests import HTTPError

#Get_Config
#A convience class to get configuration values that we do not want to show 
#(or upload to github) (key, secret, url) from a json file.It also sets up 
#logging for the helper classes. If logging is not set up, will just print 
#to the console.
#Template format is simple
#{
#   "url":"",
#   "key":"",
#   "secret":""
#}
class Get_Config():

    #Initializes the class by taking the configuration file path
    #as an argument, a typical value would be "./config.json".
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            with open(self.file_path) as conf:
                self.data = json.load(conf)
                logging.info("Configuration file loaded")
        except FileNotFoundError as e:
            logging.error('No configuration file found - Exit program')
            sys.exit()

    #Returns url value from the configuration file to a variable
    def get_url(self):
        return self.data["url"]

    #Returns key value from the configuration file to a variable
    def get_key(self):
        return self.data["key"]

    #Returns secret value from the configuration file to a variable
    def get_secret(self):
        return self.data["secret"]
    
    #(ALLY ONLY) Returns client_id from the configuration file to a variable
    def get_client_id(self):
        return self.data["client_id"]

#Auth_Helper
#A class to simplify REST API authentication for the Blackboard API.
class Auth_Helper():

    #Initializes the auth helper by taking the target system url,
    # PI key and secret as arguments.
    def __init__(self, url, key, secret):
        self.url = url
        self.key = key
        self.secret = secret

    #Returns the authentication token for Blackboard Learn.
    def learn_auth(self):
        try:
            self.url_token = "/learn/api/public/v1/oauth2/token"
            self.params = {"grant_type": "client_credentials"}
            self.headers = {
                'Content-Type': "application/x-www-form-urlencoded"}
            r = requests.request("POST", self.url+self.url_token, headers=self.headers,
                                 params=self.params, auth=(self.key, self.secret))
            r.raise_for_status()
            data = json.loads(r.text)
            self.learn_token = data["access_token"]
            logging.info("Learn Authentication successful")
            logging.info("Token expires in: "+str(data["expires_in"]))
            return self.learn_token
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["error_description"])

    #Returns the authentication token for Blackboard Collaborate.
    def collab_auth(self):
        self.token_url = '/token'
        self.exp = int(round(time.time() * 1000)) + 270000
        self.claims = {"iss": self.key, "sub": self.key, "exp": self.exp}
        # Encode the JWT assertion with the jWT module, that includes claims and the secret.
        self.assertion = jwt.encode(self.claims, self.secret)
        self.credentials = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        self.headers = {  # Content type is sent as a header
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        #Grant credentials and assertion are sent as parameters
        self.params = {  
            'grant_type': self.credentials,
            'assertion': self.assertion
        }
        try:
            r = requests.request('POST', self.url+self.token_url, params=self.params,
                                 headers=self.headers, auth=(self.key, self.secret))
            r.raise_for_status()
            data = json.loads(r.text)
            logging.info('Collaborate Authentication successful')
            logging.info("Token expires in: "+str(data["expires_in"]))
            self.collab_token = data['access_token']
            return self.collab_token
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["error"])
    
#A separate class to support Ally as a service requests.
#it is separated as it uses different authentication and has
#a still limited set of features
class Ally_Helper():

    #Initializes the auth helper by taking the target system url,
    # PI key and secret as arguments.
    def __init__(self, url, client_id, key, secret):
        self.url= url
        self.client_id= client_id
        self.key= key
        self.secret= secret

    #Returns the authentication token for Blackboard Ally. Ally does not use 
    #a post call to an endpoint, instead, it encodes a jwt assertion that then
    #is passed as a Bearer token.
    def ally_auth(self):
        self.iat= str(int(time.time()))
        self.headers= {
            'typ':'JWT',
            'alg': "Rs256"
            }
        self.claims= {
            "clientId": self.client_id ,
            "iat": self.iat
        } 
        self.assertion= jwt.encode(self.claims, self.secret).decode("utf-8")
        self.ally_token= str(self.assertion)   
        return self.ally_token

    #Uploads a file to ally service, getting the path to the file and the auth header
    #arguments
    def ally_upload_file(self, token, file_path):
        self.file_path= file_path
        self.token= token
        self.headers= {
            "Authorization":f'Bearer {self.token}'
        }
        self.ally_url= f'{self.url}/api/v2/clients/{self.client_id}/content'
        self.files= {
            'file': open(file_path,'rb')
            }
        try:
            r= requests.request('POST',self.ally_url,files= self.files,headers=self.headers)
            r.raise_for_status()
            data= json.loads(r.text)
            logging.info('File uploaded to Ally, check processing status via ally_check_status()')
            return data
        except requests.exceptions.HTTPError as e:
            logging.warning('An error occured during the request')
    
    #Returns the file hash to be used in the next requests from the upload request response
    def ally_get_hash(self,upload_response):
        self.upload_response= upload_response
        logging.info('Hash value extracted to a variable')
        return self.upload_response["hash"]

    #Checks the status of a file upload to Ally as a service, takes toekn and content hash
    #as arguments.
    def ally_check_status(self, token, content_hash):
        self.content_hash= content_hash
        self.token= token
        self.headers= {
            "Authorization":f'Bearer {self.token}'
        }
        self.check_url=f'{self.url}/api/v2/clients/{self.client_id}/content/{content_hash}/status'
        try:
            r= requests.request('GET',self.check_url,headers=self.headers)
            r.raise_for_status()
            data=json.loads(r.text)
            logging.info('status checked. See response for details')
            return data
        except requests.exceptions.HTTPError as e:
            logging.warning('An error occured during the request')

    def ally_get_feedback(self, token, content_hash,feedback=True):
        self.content_hash= content_hash
        self.token= token
        self.feedback= feedback
        self.feedback_url=f'{self.url}/api/v2/clients/{self.client_id}/content/{content_hash}'
        self.headers= {
            "Authorization":f'Bearer {self.token}'
        }
        self.params={
            "feedback":self.feedback
        }
        try:
            r= requests.request('GET',self.feedback_url,headers=self.headers,params=self.params)
            r.raise_for_status()
            data=json.loads(r.text)
            logging.info('Feedback obtained, see response for details')
            return data
        except requests.exceptions.HTTPError as e:
            logging.error('An error occured during the request', exc_info=True)

#Bb_requests
#A class to simplify API calls to Blackboard REST APIs, provides functions 
#for GET, POST, PUT, PATCH and DELETE
class Bb_requests():

    #GET request. It takes a GET endpoint from the API, the authentication
    #token and a list of parameters as arguments.
    def Bb_GET(self, endpoint, token, params):
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request('GET', self.endpoint,
                                 headers=self.headers, params=self.params)
            data = json.loads(r.text)
            r.raise_for_status()
            logging.info("GET Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])

    #POST request. It takes a POST endpoint from the API, the authentication token,
    #a list of parameters, and a json payload as arguments.
    def Bb_POST(self, endpoint, token, params, payload):
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request('POST', self.endpoint,
                                 headers=self.headers, params=self.params, json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logging.info("POST Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])

    #PATCH request. It takes a PATCH endpoint from the API, the authentication token,
    #a list of parameters, and a json payload as arguments. A PATCH requests allows
    #to update a record partially.
    def Bb_PATCH(self, endpoint, token, params, payload):
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request('PATCH', self.endpoint,
                                 headers=self.headers, params=self.params, json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logging.info("PATCH Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])

    #PUT request. It takes a PUT endpoint from the API, the authentication token, 
    #a list of parameters, and a json payload as arguments. A PUT request is meant
    #to update a record entirely.
    def Bb_PUT(self, endpoint, token, params, payload):
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.payload = payload
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request('PUT', self.endpoint,
                                 headers=self.headers, params=self.params, json=self.payload)
            data = json.loads(r.text)
            r.raise_for_status()
            logging.info("PUT Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])

    #DELETE request. It takes a DELETE endpoint from the API, the authentication token
    #and a list of parameters as arguments.
    def Bb_DELETE(self, endpoint, token, params):
        self.endpoint = endpoint
        self.token = token
        self.params = params
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': "Application/json"
        }
        try:
            r = requests.request(
                'DELETE', self.endpoint, headers=self.headers, params=self.params)
            #A successful DELETE request returns a 204 code meaning that the server has
            #fulfilled the request but that there is no content to return.
            r.raise_for_status()
            logging.info("DELETE Request completed")
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])

#A set of convenience functions (logging, printing, checking courses...), this will be extended over time.   
class Bb_Utils():

    #Sets logging with default path to ./logs and default level of DEBUG. 
    def set_logging(self, path='./logs', level=logging.DEBUG):
        self.path= path
        self.level = level
        try:
            os.mkdir(self.path,0o777)
            logging.basicConfig(
            format = '%(asctime)-15s %(name)-22s %(funcName)-15s %(levelname)-8s %(message)s',filename=f'{self.path}/Bb_helper_log_{datetime.now()}', filemode="w", level=self.level)
            logging.info('Logs folder created')
            logging.info('Logging has been set up')
        except FileExistsError:
            logging.basicConfig(
            format = '%(asctime)-15s %(name)-22s %(funcName)-15s %(levelname)-8s %(message)s',filename=f'{self.path}/Bb_helper_log_{datetime.now()}', filemode="w", level=self.level)
            logging.info('Logging has been set up')

    #Prints the response from any of the above methods in a prettified format to the console.
    def pretty_printer(self, data, sort_keys=True):
        self.data = data
        self.sort_keys = sort_keys
        if data: 
            print(json.dumps(self.data, indent=4, sort_keys=self.sort_keys))
            logging.info("Results printed to the console.")
        else:
            logging.warning("No data to print.")

    # Checks if a given Learn course exists in the server
    def check_course_id(self, course_id):
        try:
            self.endpoint_courses = "/learn/api/public/v3/courses"
            self.headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': "Application/json"
            }
            self.params = {
                "externalId": course_id,
                "fields": "id"
            }
            r = requests.request(
                'GET', self.url+self.endpoint_courses, headers=self.headers, params=self.params)
            r.raise_for_status()
            data = json.loads(r.text)
            if data["results"]:
                logging.info('The course has been found in the server.')
                return True
            else:
                logging.warning(
                    'The course could not be found, please check that the provided course id is the external id')
                return False
        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            logging.error(data["message"])
