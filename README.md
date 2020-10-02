# Bb_rest_helper (BETA)
## A Python 3 library to simplify working with Blackboard APIs

# DESCRIPTION

The Bb Rest Helper includes 4 classes to simpilfy common API operations.

1. Get_config. This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are authenticating for more than one API (i.e. Learn and Collaborate) you will need separate configuration files (i.e. learn_config.json and collab_config.json).
2. Auth_Helper. This class is used to get the token that then will be used in the API calls. Provides different functions for the different APIs.
3. Bb_requests. This calsses is used to simplify calls to the Blackboard Rest APIs, provides functions for GET, POST, PUT, PATCH and DELETE requests.
4. Bb_utils. A set of convenience functions (printing, checking courses...) 

# SETUP.

1. Register a new application in the developer portal, grab key, secret and application id.
2. Configure the application in your Learn instance, you will need the application id and a user with the right permissions. DO NOT USE AN ADMIN USER!
3. Fill the configuration template (config.json).
4. OPTIONAL--> Create a python3 virtual environment.
5. Install dependencies via the requirement file. "Pip3 install requirements.txt".
6. Make the Bb_rest_helper.py file is in the parent directory for your application.

# USAGE.

1. Imports:
    ```
    from Bb_rest_helper import Get_Config
    from Bb_rest_helper import Auth_Helper
    from Bb_rest_helper import Bb_requests
    from Bb_rest_helper import Bb_Utils
    ```
2. create an instance of the Get_config class to get configuration values from a Json file: 
    ```
    #create an instance of the Get_config class
    config=Get_Config('./collab_config.json')

    #Get configuration values
    url=config.get_url()
    key=config.get_key()
    secret=config.get_secret()
    ```
    if using more than one API, you will need to use separate configuration files
    
    ```
    #Get Collab credentials
    collab_config=Get_Config('./collab_config.json')
    
    collab_url=collab_config.get_url()
    collab_key=collab_config.get_key()
    collab_secret=collab_config.get_secret()
    
    #Get Learn credentials
    learn_config=Get_Config('./learn_config.json')
    
    learn_url=learn_config.get_url()
    learn_key=learn_config.get_key()
    learn_secret=learn_config.get_secret()
    ```
4. Get the authentication token by creating an instance of the auth method, and then calling the relevant auth function:
    ```
    #Collaborate
    collab_auth=Auth_Helper(collab_url,collab_key,collab_secret)
    collab_token=collab_auth.collab_auth()
    
    #Learn
    learn_auth=Auth_helper(learn_url,learn_key,learn_secret)
    learn_token=learn_auth.learn_auth()
    
    ```
5. Example GET call:

* Create variables for the API endpoint url and the request parameters. The whole endpoint url (i.e https//myserver.blackboard.com/learn/api/public/v3/courses)     needs to be provided  
    ```
    #Learn GET Courses endpoint and params example
    courses_endpoint=f'{learn_url}/learn/api/public/v3/courses"
    params={
        'limit':'10',
        'fields':'courseId,name,description,ultraStatus'
          }
          
    #Collaborate GET Sessions endpoint and params example
    session_endpoint=f'{url}/sessions'
    params={
        "limit":"10"
    }
     ```   
* Create an instance of Bb_requests, then call the Bb_GET method pasing the endpoint, token and parameters as arguments.
    ```
    #Create an instance of the Bb_requests class
    reqs=Bb_requests()
    
    #Learn GET example
    learn_data=reqs.Bb_GET(courses_endpoint,learn_token,params)
    
    #Collab GET example
    collab_data=reqs.Bb_GET(session_endpoint,collab_token,params)
    ```
* Create an instace of teh Bb_utils class, then Use the pretty_printer method to print the  results to the console
    ```
    #Create an instance of the Bb_utils class
    utils=Bb_utils()
    
    # Uuse the pretty printer method to print results to the console
    helper.pretty_printer(GET_course)
    ```
