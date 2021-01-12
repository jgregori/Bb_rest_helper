# Bb_rest_helper.
## A Python 3 library to simplify working with Blackboard APIs.

This library is intended to explore Blackboard REST APIs and to help create POCs for integrations. **This tool is not intended to be used in production and no warranties of any kind are provided.** 

# DESCRIPTION.

The Bb Rest Helper includes 5 classes to simpilfy common API operations with Blackboard APIs;

1. **Get_Config.** This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are authenticating for more than one API (i.e. Learn and Collaborate) you will need separate configuration files (i.e. learn_config.json and collab_config.json).
2. **Auth_Helper.** This class is used to get the token that then will be used in the API calls. Provides different methods for the different APIs.
3. **Bb_Requests.** This class is used to simplify calls to the Blackboard Rest APIs. Provides methods for GET, POST, PUT, PATCH and DELETE requests.
4. **Bb_Utils.** A set of convenience functions (Logging, printing...), this will be extended over time.
5. **Ally_Helper** This class is used to simplify interaction with Ally as a service, includes methods to authenticate, upload a file, check processing status and retrieve the feedback. As it is an initial release for this API with limited features, it is implemented as a separate class to provide easier access to these methods rather than having to code them manually or with the Bb_rest_helper library.

# SETUP. Make sure you are at least in Python 3.7+!

The first step is to get the right credentials for the API that you will be using. Depending on the API, the process may be a bit different, we offer a summary, but please check docs.blackboard.com for the full picture.

## For Blackboard Learn:

1. **Register a new application** in the Blackboard developer portal (developer.blackboard.com), grab key, secret and application id.
2. **Configure the application in your Learn instance**. You will need the application id and a user with the right permissions. **DO NOT USE AN ADMIN USER!**
3. **Fill the configuration template (config.json).** You may want to rename to "learn_config.json" to keep track of the changes.

## For Blackboard Collaborate:

1. **Use REST API credentials or LTI integration credentials.** REST credentials are standalone (not connected to your institution´s login group) and can be
   obtained by writing to developers@blackboard.com. LTI credentials are the same that you would use to configure Collaborate in your LMS, and can be obtained
   from Blackboard support. Any changes in your production system as a result of API testing are at your sole responsability.
2. **Fill the configuration template (config.json).** you may want to rename to "collab_config.json" to keep track of the changes.

## For ALLY as a service:

1. **You need a client id, key and secret.** At this time, the best way to obtain this information is to engage your Account Executive to discuss pricing and 
   request credentials. As the API continues to grow, this process may change.
2. **Fill the configuration template (config.json).** you may want to rename to "Ally_config.json" to keep track of the changes.

# ENVIRONMENT SETUP.

Once you have the right credentials in place and your application is registered (if needed). You need to set up your environment:

1. **OPTIONAL--> Create a python3 virtual environment.** A virtual environment will provide you with a separate and clean instalation of Python just for the
   project you are working on, this is really helpful to avoid issues with libraries and dependencies across projects. You can create a virtual environment by
   installing the virtualenv python library
    
         pip3 install virtualenv
    
    then you create a virtual environment by navigating to the desired folder for your application and using the command:
    
         python3 -m venv env 
    
    you can activate this virtual environment by using the command:
         
         source env/bin/activate
    
    Once you are done, you can just deactivate the virtual environment by using:
    
         deactivate
    
2. **Install the Bb_rest_helper package from PYPI (using PIP).** To do this, simply use the PIP command or PIP3, depending on how your python  was installed.
   
         pip3 install Bb-rest-helper
  
# USAGE.

1. Imports:
    
       #Import the classes that you need!
       from Bb_rest_helper import Get_Config
       from Bb_rest_helper import Auth_Helper
       from Bb_rest_helper import Bb_Requests
       from Bb_rest_helper import Bb_Utils
       from Bb_rest_helper import Ally_Helper
    
2. create an instance of the Get_Config class to get configuration values from a JSON file: 
    
       #create an instance of the Get_Config class.
       config=Get_Config('./collab_config.json')

       #Get configuration values
       url=config.get_url()
       key=config.get_key()
       secret=config.get_secret()
    
    If using more than one API, you will need to use separate configuration files.
    
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
    
    Note that if the path of the configuration file is incorrect, the program will be terminated and an error will be logged. Make sure that your configuration
    files are in the right path.

   Configure the logging, otherwise the application will run, but will not provide any info. To do so create an instance of the Bb_utils class and set the
   logging by using the set_logging() method.
    
       #Create an instance of the Bb_utils class
       utils=Bb_utils()
       #Set the logging, default does not require arguments
       utils.set_logging()
    
    Default logging level is DEBUG, but this can be changed by passing the desired level value to the set_logging method. it is also possible to change the path
    for the logs folder, but currently only within the the main folder of the application.

         config.set_logging('logging.WARNING','./different_folder')
   
3. Get the authentication token by creating an instance of the auth method, and then calling the relevant auth function:
    
       #Collaborate
       collab_auth=Auth_Helper(collab_url,collab_key,collab_secret)
       collab_token=collab_auth.collab_auth()

       #Learn
       learn_auth=Auth_Helper(learn_url,learn_key,learn_secret)
       learn_token=learn_auth.learn_auth()

       #Ally
       #Note ally is part of a separate class, and different methods apply
       ally_auth=Ally_Helper(ally_url, client_id, ally_key, ally_secret)
       ally_token=ally_auth.ally_auth()
   
4. Example GET call:

   Create variables for the API endpoint url and the request parameters. The whole endpoint url (i.e https//myserver.blackboard.com/learn/api/public/v3/courses)
   needs to be provided.

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
       
   If you do not wish to use params, pass an empty dictionary:
    
         params={}
   
   Create an instance of Bb_Requests, then call the Bb_GET method pasing the endpoint, token and parameters as arguments.
    
         #Create an instance of the Bb_Requests class
         reqs=Bb_Requests()
    
         #Learn GET example
         learn_data=reqs.Bb_GET(courses_endpoint,learn_token,params)
    
         #Collab GET example
         collab_data=reqs.Bb_GET(session_endpoint,collab_token,params)
    
   Create an instance of the Bb_utils class, then Use the pretty_printer method to print the results to the console
    
         #Create an instance of the Bb_utils class
         utils=Bb_utils()
    
         # Uuse the pretty printer method to print results to the console
         helper.pretty_printer(GET_course)
    
5. Differences between a **POST, PUT, PATCH** requests.

    The only difference is that these requests need an additional JSON payload, as per the API definition, to be able to create and/or update records, also the
    right method needs to be selected from the Bb_request class (i.e. Bb_POST for a post request).
     
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

6. **Bb_Utils class**         
    
    Bb_Utils is a class that contains utiliy methods that make our life easier when performing certain common operations with the Blackboard REST APIs such as
    logging, pretty printing, date formatting or id conversion. This class is somewhat experimental and will be growing over time as the need arises in new
    projects. Here is a brief explanation of the methods in this class:


    The first step to use the methods is to create an isntance of the Bb_utils class:
        
        utils = Bb_Utils()

    **set_logging** This method has been coverd in detail in section 2 of this document.
    
    **pretty_printer** Prints the response from any of the requests methods in a prettified format to the console.
        
        courses = reqs.Bb_GET(url_courses,learn_token,params) #Example call. 
        utils.pretty_printer(courses)
        
        by default, the method will indent 4 spaces and sort the keys aphabetically, this can be modified by passing sort_keys = False as a second argument
        
        utils.pretty_printer(courses, sort_keys = False)
        

    **check_course_id** Checks if a given Learn course exists in the server by taking the external course id as an 
    argument and returs True or False. Please note that the accuracy of this method depends on the externalId being an specific value. It is discouraged to use short, commong strings such as 001 or aaa as those would likely return many different values.
          
          check_course = utils.(external_course_id) #Returns True or False.
          
    **time_format**  This method is provided to facilitate date formatting when importing dates from  other applications, i.e, dates in excel format, it can take a 
        date string with the following formats

            DD/MM/YYYY
            DD/MM/YYYY HH:MM
            DD/MM/YYYY HH:MM:SS

        optional arguments for date delimiter (default "/") and hour delimiter (default ":")
        can be provided. The outcome of the method is YYYY-MM-DDTHH:MM:SS:000Z
        
        formatted_date = utils.time_format(DD/MM/YYYY)

    **learn_convert_external_id**  This method is used to get the external id of a learn course as an argument
         and return another field in the get response (usually the course id). We found it is a common operation, particularly when getting a list of courses in a CSV.
         
         converted_id = utils.learn_convert_external_id(learn_url, learn_token,'007687') 
         #Returns the courseId (default)
         

        if interested in converting the externalId to another value that can be found in the get response for courses, pass that field name as the last argument for the method
         
         conv_id = utils.learn_convert_external_id(learn_url, learn_token,'007687','DataSourceId') 
         #Returns the dataSourceId instead of the id
         

        formatted_date = utils.time_format(DD/MM/YYYY)
     
   **learn_convert_external_id**  This method is used to get the external id of a learn course as an argument and return another field in the get response
   (usually the course id). We found it is a common operation, particularly when getting a list of courses in a CSV.
       
         converted_id = utils.learn_convert_external_id(learn_url, learn_token,'007687') 
         #Returns the courseId (default)
      
   If interested in converting the externalId to another value that can be found in the get response for courses, pass that field name as the last argument for
   the method.
        
         converted_id = utils.learn_convert_external_id(learn_url, learn_token,'007687','DataSourceId') 
         #Returns the dataSourceId instead of the id
         
7. **Ally Helper usage**

    Get the athentication token as described in section 3
    
         #Ally
         #Note ally is part of a separate class, and different methods apply
         ally_auth=Ally_Helper(ally_url, client_id, ally_key, ally_secret)
         ally_token=ally_auth.ally_auth()
    
    Upload a file to be checked for accesibility, providing the token and the file path. Make sure to provide a supported file
    
         upload=ally_upload_file(ally_token,'./file.docx')
    
    Use the ally_get_hash() method to easily get the the file hash from the upload request response.
    
         file_hash= ally_get_hash(upload)
    
    Check status of the file processing by pasing the token and file hash as arguments to the check status method.
   
         check= ally_check_status(ally_token,file_hash)
    
    Get the accesibility feedback for the file from the get feedback method by passing the token and content hash. 
    
         feedback= ally_get_feedback(ally_token, file_hash)
    

