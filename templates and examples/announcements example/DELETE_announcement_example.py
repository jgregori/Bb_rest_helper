#imports
from Bb_rest_helper import Get_Config
from Bb_rest_helper import Auth_Helper
from Bb_rest_helper import Bb_Requests
from Bb_rest_helper import Bb_Utils

def main():
    
   #Initialize an instance of the Get_Config class, passing the file path of the configuration file as argument.
    config=Get_Config("./learn_config.json")

    #Get configration values from config.json.
    url=config.get_url()
    key=config.get_key()
    secret=config.get_secret()

    #Set logging
    utils= Bb_Utils()
    utils.set_logging()

    #Authentication
    auth= Auth_Helper(url,key,secret)
    token= auth.learn_auth()

    #Prepare the request  
    announcement_id='_966_1' #replace with the actual annoucement ID from the POST announcements example
    DELETE_announcements_endpoint=f'{url}/learn/api/public/v1/announcements/{announcement_id}'
    params={
        'fields':'id,title,body'
        }   

    #request
    req= Bb_Requests()
    DELETE_announcements=req.Bb_DELETE(DELETE_announcements_endpoint,token,params)


 
if __name__ == "__main__":
    main()
