#A starter template for the Bb_rest_helper libraray.
#Check documentation for usage details.

#imports.
from Bb_rest_helper import Bb_Utils
from Bb_rest_helper import Get_Config
from Bb_rest_helper import Auth_Helper
from Bb_rest_helper import Bb_Requests

from Bb_rest_helper import Ally_Helper

#logging.
utils = Bb_Utils()
utils.set_logging()

#Get credentials from file. If using several API
#you need to repeat this process.

#Learn.
learn_conf = Get_Config('./learn_config.json')
learn_url = learn_conf.get_url()
learn_key = learn_conf.get_key()
learn_secret = learn_conf.get_secret()
#Collaborate.
collab_conf = Get_Config('./collab_config.json')
collab_url = collab_conf.get_url()
collab_key = collab_conf.get_key()
collab_secret = collab_conf.get_secret()
#Ally.
ally_conf = Get_Config('./ally_config.json')
ally_url = ally_conf.get_url()
ally_key = ally_conf.get_key()
ally_secret = ally_conf.get_secret()
ally_clientId = ally_conf.get_client_id()

#Authenticate and get the token (Learn).
learn_auth = Auth_Helper(learn_url, learn_key, learn_secret)
learn_token = learn_auth.learn_auth()

#Authentitcate and get the token (Collaborate).
collab_auth = Auth_Helper(collab_url, collab_key, collab_secret)
collab_token = collab_auth.collab_auth()

#Authenticate and get the token (Ally).
ally_auth = Ally_Helper(ally_url, ally_clientId, ally_key, ally_secret)
ally_auth = ally_auth.ally_auth()

#Rest API calls
reqs = Bb_Requests()

#Example Collaborate GET sessions request (limited to the 10 first results)
sessions_url= f'{collab_url}/sessions'
params = {
    "limit":"10"
}
sessions = reqs.Bb_GET(sessions_url, collab_token, params)
utils.pretty_printer(sessions)

#Example Learn POST Calendar request with no parameters.
calendar_url = f'{learn_url}/learn/api/public/v1/calendars/items'
params = {}
payload= {
    "type": "Course",
    "calendarId":"_122_1",
    "title": "Test session",
    "description": "This is a sample payload, note the calendar id is the course id",
    "location": "Room 25",
    "start": "2020-11-06T14:36:47.666Z",
    "end": "2020-11-06T15:36:47.666Z"
    }
calendar = reqs.Bb_POST(calendar_url, learn_token, params, payload)
utils.pretty_printer(calendar, sort_keys= False)

#Example Ally, get feedback for uploaded file.
upload = ally_upload_file(ally_token,'./file.docx')
file_hash = ally_get_hash(upload)
check = ally_check_status(ally_token, file_hash)
feedback = ally_get_feedback(ally_token, file_hash)

