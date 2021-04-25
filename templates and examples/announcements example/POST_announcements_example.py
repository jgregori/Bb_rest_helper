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
    auth=Auth_Helper(url,key,secret)
    token=auth.learn_auth()

    #Prepare the request   
    POST_announcements_endpoint=f'{url}/learn/api/public/v1/announcements'
    params={
        'fields':'id,title,body'
         }

    payload={
        "title": "Javier API TEST",
        "body": "<!-- {\"bbMLEditorVersion\":1} --><div data-bbid=\"bbml-editor-id_9c6a9556-80a5-496c-b10d-af2a9ab22d45\"> <h4>Header Large</h4>  <h5>Header Medium</h5>  <h6>Header Small</h6>  <p><strong>Bold&nbsp;</strong><em>Italic&nbsp;<span style=\"text-decoration: underline;\">Italic Underline</span></em></p> <ul>   <li><span style=\"text-decoration: underline;\"><em></em></span>Bullet 1</li>  <li>Bullet 2</li> </ul> <p>  <img src=\"@X@EmbeddedFile.requestUrlStub@X@bbcswebdav/xid-1217_1\">   <span>\"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\"</span> </p>  <p><span>&lt;braces test=\"values\" other=\"strange things\"&gt;</span></p> <p>Header Small</p> <ol>   <li>Number 1</li>   <li>Number 2</li> </ol>  <p>Just words followed by a formula</p>  <p><img align=\"middle\" alt=\"3 divided by 4 2 root of 7\" class=\"Wirisformula\" src=\"@X@EmbeddedFile.requestUrlStub@X@sessions/EA5F7FF3DF32D271D0E54AF0150D924A/anonymous/wiris/49728c9f5b4091622e2f4d183d857d35.png\" data-mathml=\"«math xmlns=¨http://www.w3.org/1998/Math/MathML¨»«mn»3«/mn»«mo»/«/mo»«mn»4«/mn»«mroot»«mn»7«/mn»«mn»2«/mn»«/mroot»«/math»\"></p> <p><a href=\"http://www.blackboard.com\">Blackboard</a></p> </div>",
        "availability": {
            "duration": {
                "type": "Permanent",
                },
            },
        "showAtLogin": True,
        "showInCourses": False,
        }

    #request
    req= Bb_Requests()
    POST_announcements=req.Bb_POST(POST_announcements_endpoint,token,params,payload)


    #Pretty print results to the console.
    utils.pretty_printer(POST_announcements)

if __name__ == "__main__":
    main()
