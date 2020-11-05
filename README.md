# Bb_rest_helper (BETA)
## A Python 3 library to simplify working with Blackboard APIs

# DESCRIPTION

The Bb Rest Helper includes 4 classes to simpilfy common API operations.

1. **Get_Config.** This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are             authenticating for more than one API (i.e. Learn and Collaborate) you will need separate configuration files (i.e. learn_config.json and collab_config.json).
2. **Auth_Helper.** This class is used to get the token that then will be used in the API calls. Provides different methods for the different APIs.
3. **Bb_Requests.** This class is used to simplify calls to the Blackboard Rest APIs. Provides methods for GET, POST, PUT, PATCH and DELETE requests.
4. **Bb_Utils.** A set of convenience functions (Logging,printing, checking courses...), this will be extended over time.
5. **Ally_Helper** This class is used to simplify interaction with Ally as a service, includes methods to authenticate, upload a file, check processing status and retrieve the feedback. As it is an initial release for this API with limited features, it is implemented as a separate class to provide easier access to these methods rather than having to code them manually or with the Bb_helper library.

# SETUP. Make sure you are at least in Python 3.7+!

The first step is to get the right credentials for the API that you will be using. Depending on the API, the process may be a bit different

## For Blackboard Learn:
1. **Register a new application** in the Blackboard developer portal (developer.blackboard.com), grab key, secret and application id.
2. **Configure the application in your Learn instance**. You will need the application id and a user with the right permissions. DO NOT USE AN ADMIN USER!
3. **Fill the configuration template (config.json).** You may want to rename to "learn_config.json" to keep track of the changes.

## For Blackboard Collaborate:
1. **Use REST API credentials or LTI integration credentials.** REST credentials are standalone (not connected to your institution´s login group) and can be obtained by writing to developers@blackboard.com. LTI credentials are the same that you would use to configure Collaborate in your LMS, and can be obtained from Blackboard support. Any changes in your production system as a result of API testing is at your sole responsability.
2. **Fill the configuration template (config.json).** you may want to rename to "collab_config.json" to keep track of the changes.

## For ALLY as a service.
1. **You need a client id, key and secret.** At this time, the best way to obtain this information is to engage your Account Executive to discuss pricing and request credentials. As the API continues to grow, this process may chang
2. **Fill the configuration template (config.json).** you may want to rename to "Ally_config.json" to keep track of the changes.

Once you have the right credentials in place and your application is registered (if needed). You need to set up your environment.

1. **OPTIONAL--> Create a python3 virtual environment.** A virtual environment will provide you with a separate and clean instalation of Python just for the project you are working on, this is really helpful to avoid issues with libraries and dependencies across projects.
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
  
2. **Install dependencies via the requirements.txt file.** (if you are using a virtual environment, make sure it is active before installing dependencies/libraries, otherwise you will be installing those in your global python environment)
    ```
    Pip3 install -r requirements.txt
    ```
3. **Make sure the Bb_rest_helper.py file is in the parent directory for your application.**

# USAGE.

1. Imports:
    ```
    #Use the ones that you need!
    from Bb_rest_helper import Get_Config
    from Bb_rest_helper import Auth_Helper
    from Bb_rest_helper import Bb_requests
    from Bb_rest_helper import Bb_Utils
    from Bb_rest_helper import Ally_Helper
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
    If using more than one API, you will need to use separate configuration files
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
    Configure the logging, otherwise the application will run, but will not provide any info. To do so create an instance of the Bb_utils class and set the logging
    ```
    #Create an instance of the Bb_utils class
    utils=Bb_utils()
    #Set the logging, default does not require arguments
    utils.set_logging()
    ````
    Default logging level is DEBUG, but this can be changed by passing the desired level value to the set_logging method. it is also possible to change the path for the logs folder, but currently only within the the main folder of the application.
    ```
    config.set_logging('logging.WARNING','./different_folder')
    ```
3. Get the authentication token by creating an instance of the auth method, and then calling the relevant auth function:
    ```
    #Collaborate
    collab_auth=Auth_Helper(collab_url,collab_key,collab_secret)
    collab_token=collab_auth.collab_auth()
    
    #Learn
    learn_auth=Auth_helper(learn_url,learn_key,learn_secret)
    learn_token=learn_auth.learn_auth()

    #Ally
    #Note ally is part of a separate class, and different methods apply
    ally_auth=Ally_Helper(ally_url, client_id, ally_key, ally_secret)
    ally_token=ally_auth.ally_auth()
    ```
4. Example GET call:

Create variables for the API endpoint url and the request parameters. The whole endpoint url (i.e https//myserver.blackboard.com/learn/api/public/v3/courses)     needs to be provided  
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
If you do not wish to use params, pass an empty dictionary:
    ```
    params={}
    ```
Create an instance of Bb_requests, then call the Bb_GET method pasing the endpoint, token and parameters as arguments.
    ```
    #Create an instance of the Bb_requests class
    reqs=Bb_requests()
    
    #Learn GET example
    learn_data=reqs.Bb_GET(courses_endpoint,learn_token,params)
    
    #Collab GET example
    collab_data=reqs.Bb_GET(session_endpoint,collab_token,params)
    ```
Create an instace of teh Bb_utils class, then Use the pretty_printer method to print the  results to the console
    ```
    #Create an instance of the Bb_utils class
    utils=Bb_utils()
    
    # Uuse the pretty printer method to print results to the console
    helper.pretty_printer(GET_course)
    ```
5. Differences between a **POST, PUT, PATCH** requests.

    The only difference is that these requests need an additional JSON payload, as per the API definition, to be able to create and/or update records, also the right method needs to be selected from the Bb_request class (i.e. Bb_POST for a post request).
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
6. **Ally Helper usage**

    Get the athentication token as described in section 3
    ```
    #Ally
    #Note ally is part of a separate class, and different methods apply
    ally_auth=Ally_Helper(ally_url, client_id, ally_key, ally_secret)
    ally_token=ally_auth.ally_auth()
    ```
    Upload a file, providing the token and the file path.
    ```
    upload=ally_upload_file(ally_token,'./file.docx')
    ```
    Use the ally_get_hash() method to easily get the the file hash from the upload request response.
    ```
    file_hash= ally_get_hash(upload)
    ```
    Check status of the file processing by pasing the token and file hash as arguments to the check status method.
    ```
    check= ally_check_status(ally_token,file_hash)
    ```
    Get the accesibility feedback for the file from the get feedback method by passing the token and content hash. 
    ```
    feedback= ally_get_feedback(ally_token, file_hash)
    ```

