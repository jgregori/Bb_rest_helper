from datetime import datetime
import json
import requests
from requests import HTTPError
import logging

# Get_Config
#############
# A convience class to get configuration values that we do not want to show (or upload to github) (key, secret, url) from a json file.
# Template format is simple
# {
#   "url":"",
#   "key":"",
#   "secret":"" 
# }
class Get_Config():

    #Initializes the class by taking the configuration file path as an argument, my typical value would be "./config.json".
    def __init__(self,file_path):
        self.file_path=file_path
        with open(self.file_path) as conf:
            self.data=json.load(conf)

    #Returns url value from the configuration file to a variable of choice
    def get_url(self):
        return self.data["url"]

    #Returns key value from the configuration file to a variable of choice
    def get_key(self):
        return self.data["key"]

    #Returns secret value from the configuration file to a variable of choice
    def get_secret(self):
        return self.data["secret"]

# Learn_Helper 
###############
# A class to simplify GET, POST, PATCTH and DELETE requests to the Blackboard REST API.            
class Learn_Helper():

    #Initializes the Learn Api helper by taking the target system url, API key and secret (from the dev portal) as arguments.
    def __init__(self,url,key,secret):
        self.learn_url=url
        self.learn_key=key
        self.learn_secret=secret
        logging.basicConfig(filename=f'./logs/learn_helper_log_{datetime.now()}',filemode="w",level=logging.DEBUG)
        
    #Returns the authentication token. 
    def learn_authenticate(self):
        try:
            self.url_token="/learn/api/public/v1/oauth2/token" #POST
            self.params={"grant_type":"client_credentials"}
            self.headers={'Content-Type': "application/x-www-form-urlencoded"}
            r=requests.request("POST",self.learn_url+self.url_token,headers=self.headers,params=self.params,auth=(self.learn_key, self.learn_secret))
            r.raise_for_status()
            data=json.loads(r.text)
            self.token=data["access_token"]
            logging.info("Authentication successful")
            logging.info("Token expires in: "+str(data["expires_in"]))
            return self.token
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["error_description"])
            
    #GET request. it takes a GET endpoint from the API, the authentication token and a list of parameters.
    def learn_GET(self,endpoint,token,params):
        self.endpoint=endpoint
        self.token=token
        self.params=params
        self.headers={
            'Authorization':f'Bearer {self.token}',
            'Content-Type':"Application/json"
            }
        try:
            r=requests.request('GET',self.learn_url+self.endpoint,headers=self.headers,params=self.params)
            data=json.loads(r.text)
            r.raise_for_status()
            logging.info("GET Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["error_description"])

    #POST request. it takes a POST endpoint from the API, the authentication token, a list of parameters, and a json payload.
    def learn_POST(self,endpoint,token,params,payload):
        self.endpoint=endpoint
        self.token=token
        self.params=params
        self.payload=payload
        self.headers={
            'Authorization':f'Bearer {self.token}',
            'Content-Type':"Application/json"
            }
        try:
            r=requests.request('POST',self.learn_url+self.endpoint,headers=self.headers,params=self.params,json=self.payload)
            data=json.loads(r.text)
            r.raise_for_status()
            logging.info("POST Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["message"])

    #PATCH request. it takes a PATCH endpoint from the API, the authentication token, a list of parameters, and a json payload.
    def learn_PATCH(self,endpoint,token,params,payload):
        self.endpoint=endpoint
        self.token=token
        self.params=params
        self.payload=payload
        self.headers={
            'Authorization':f'Bearer {self.token}',
            'Content-Type':"Application/json"
            }
        try:
            r=requests.request('PATCH',self.learn_url+self.endpoint,headers=self.headers,params=self.params,json=self.payload)
            data=json.loads(r.text)
            r.raise_for_status()
            logging.info("PATCH Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["message"])

    #DELETE request. it takes a DELETE endpoint from the API, the authentication token and a list of parameters.
    def learn_DELETE(self,endpoint,token,params):    
        self.endpoint=endpoint
        self.token=token
        self.params=params
        self.headers={
            'Authorization':f'Bearer {self.token}',
            'Content-Type':"Application/json"
            }
        try:
            r=requests.request('DELETE',self.learn_url+self.endpoint,headers=self.headers,params=self.params)
            data=json.loads(r.text)
            r.raise_for_status()
            logging.info("DELETE Request completed")
            return data
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["message"])

    #Prints the response from any of the above methods in a prettified format to the console.
    def pretty_printer(self,data):
        self.data=data
        print(json.dumps(self.data,indent=4,sort_keys=True))
        logging.info("Results printed to the console.")    

    #Checks if a given course exists in the server
    def check_course_id(self,course_id):
        try:
            self.endpoint_courses="/learn/api/public/v3/courses" #GET
            self.headers={
                'Authorization':f'Bearer {self.token}',
                'Content-Type':"Application/json"
                }
            self.params={
                "externalId":course_id,
                "fields":"id"
                }
            r=requests.request('GET',self.learn_url+self.endpoint_courses,headers=self.headers,params=self.params)
            r.raise_for_status()
            data=json.loads(r.text)
            if data["results"]:
                logging.info('The course has been found in the server.')
                return True
            else:
                logging.warning('The course could not be found, pelase check that the provided course id is the external id')
                return False
        except requests.exceptions.HTTPError as e:
            data=json.loads(r.text)
            logging.error(data["message"])