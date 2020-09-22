# Bb_rest_helper
A class to simplify GET, POST, PATCTH and DELETE requests to the Blackboard REST API

SETUP.

1. Register a new application in the developer portal, grab key, secret and application id.
2. Configure the application in your Learn instance, you will need the application id and a user with the right permissions. DO NOT USE AN ADMIN USER!
3. Fill the configuration template (config.json).
4. OPTIONAL--> Create a python3 virtual environment.
5. Install dependencies via the requirement file. "Pip3 install requirements.txt".
6. Make the Bb_rest_helper.py file is in the parent directory for your application.

USAGE.

1. Imports:
    
    from Bb_rest_helper import Get_Config
    from Bb_rest_helper import Learn_Helper
    
2. Get configuration values: 

    url=config.get_url()
    key=config.get_key()
    secret=config.get_secret()
    
3. Initialize an instance of the Learn Helper class, passing url, key and secret as arguments:

    helper=Learn_Helper(url,key,secret)
    
4. Get the authentication token:

    token=helper.learn_authenticate()
    
5. Example GET call:

5.1. Create variables for the API endpoint url and the request parameters 

    GET_courses_endpoint="/learn/api/public/v3/courses"
    params={
        'limit':'10',
        'fields':'courseId,name,description,ultraStatus'
          }
          
5.2. Call the learn_GET method, pasing the endpoint, token and parameters

    GET_course=helper.learn_GET(GET_courses_endpoint,token,params)

5.3. Use the pretty_printer method to print the call results to the console

    helper.pretty_printer(GET_course)
