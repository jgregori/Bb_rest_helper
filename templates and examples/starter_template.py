#A starter template for the Bb_rest_helper library.
#Check documentation for usage details.

#imports.
from Bb_rest_helper import Bb_Utils
from Bb_rest_helper import Get_Config
from Bb_rest_helper import Auth_Helper
from Bb_rest_helper import Bb_Requests

#logging and utils initialization.
utils = Bb_Utils()
utils.set_logging()

#Authenticate and get the token (Learn).
#V3 updates this method so passing the platform as an argument is no longer needed.
#Leaving as V2 until V3 is relased
quick_auth_learn = utils.quick_auth('./credentials/config.json','Learn')

#Retrieve token and server url
learn_token = quick_auth_learn['token']
learn_url = quick_auth_learn['url']

print(learn_token,learn_url)

#Initialize Rest API calls
reqs = Bb_Requests()

#Your code goes here