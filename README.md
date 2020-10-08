# Bb_rest_helper (BETA)
## A Python 3 library to simplify working with Blackboard APIs

# DESCRIPTION

The Bb Rest Helper includes 4 classes to simpilfy common API operations.

1. **Get_config.** This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are             authenticating for more than one API (i.e. Learn and Collaborate) you will need separate configuration files (i.e. learn_config.json and collab_config.json).
2. **Auth_Helper.** This class is used to get the token that then will be used in the API calls. Provides different functions for the different APIs.
3. **Bb_requests.** This class is used to simplify calls to the Blackboard Rest APIs. Provides functions for GET, POST, PUT, PATCH and DELETE requests.
4. **Bb_utils.** A set of convenience functions (printing, checking courses...), this will be extended over time.

# SETUP. Make sure you are at least in Python 3.7+!

1. **Register a new application** in the Blackboard developer portal (developer.blackboard.com), grab key, secret and application id.
2. **Configure the application in your Learn instance** ,you will need the application id and a user with the right permissions. DO NOT USE AN ADMIN USER!
3. **Fill the configuration template (config.json).**
4. **OPTIONAL--> Create a python3 virtual environment.** A virtual environment will provide you with a separate and clean instalation of Python just for the        project you are working on, this is really helpful to avoid issues with libraries and dependencies across projects.
   You can create a virtual environment by installint the virtualenv python librarly
    ```
    Pip3 install virtualenv
    ```
    then you create a virtual environment by navigating to the desired folder for your application and using the command:
     ```
    Python3 -m venv env 
    ```
    you can activate this virtual environment by using the command:
    ```
    source env/bin/activate
    ```
    Once you are done, you can just deactivate the virtual environment by using:
    ```
    deactivate
    ```
  
5. **Install dependencies via the requirements.txt file.** (if you are using a virtual environment, make sure it is active before installing                  dependencies/libraries, otherwise you will be installing those in your global python environment)
    ```
    Pip3 install -r requirements.txt
    ```
6. **Make sure the Bb_rest_helper.py file is in the parent directory for your application.**

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
    * if using more than one API, you will need to use separate configuration files
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
    * configure the logging, otherwise the application will run, but will not provide any info
    ```
    config.set_logging()
    ````
    * default logging level is DEBUG, but this can be changed by passing the Debug level value to the set_logging method
    ```
    config.set_logging('logging.WARNING')
    ```
3. Get the authentication token by creating an instance of the auth method, and then calling the relevant auth function:
    ```
    #Collaborate
    collab_auth=Auth_Helper(collab_url,collab_key,collab_secret)
    collab_token=collab_auth.collab_auth()
    
    #Learn
    learn_auth=Auth_helper(learn_url,learn_key,learn_secret)
    learn_token=learn_auth.learn_auth()
    ```
4. Example GET call:

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
* if you do not wish to use params, pass an empty dictionary:
    ```
    params={}
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
5. Differences with a **POST, PUT, PATCH** requests.

    the only difference is that these requests need an additional JSON payload, as per the API definition, to be able to create and/or update records, also the       right method needs to be selected from the Bb_request class (i.e. Bb_POST for a post request)
     ```
        #example of a json payload to create courses in Learn
        payload={
        "externalId": "Javier_API_003",
        "courseId": "Javier_API_003",
        "name": "Learn helper test",
        "description": "A learn helper test to check if the class works as expectted",
        "organization": False,
        "ultraStatus": "Ultra",
        "availability": {
            "available": "Yes",
            "duration": {
            "type": "Continuous",
                },
            },
        }
        ```
    
    
