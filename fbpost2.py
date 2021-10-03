import json
import os
from requests_toolbelt import MultipartEncoder
import requests
import sys
from config import returnConfig

apiConfig = returnConfig()
file_location = apiConfig.get("storage","filePath")
fb_page_access_token = apiConfig.get("api_keys","fb_page_access_token")

header = {'Content-Type': 'multipart/form-data'}
team = sys.argv[1]
sub_id = sys.argv[2]
data = {
        'message': json.dumps({
            'attachment': {
                'type': 'video',
                'payload': {}
            }
        }),
        'filedata': (os.path.basename(file_location+team+'.mp4'), open('/home/montyv36/'+team+'.mp4', 'rb'), 'video/mp4')
    }

params = {'access_token': fb_page_access_token}
multipart_data2 = MultipartEncoder(data)

multipart_header = {
        'Content-Type': multipart_data2.content_type
    }

print(multipart_data2)
r = requests.post("https://graph.facebook.com/v9.0/me/message_attachments", params=params, headers=multipart_header, data=multipart_data2,verify = False)
print(r.text)
a = r.json()["attachment_id"]
print(a)

url = "https://graph.facebook.com/v9.0/me/messages?access_token="+fb_page_access_token
payload = "{\n  \"recipient\":{\n    \"id\":\""+sub_id+"\"\n  },\n  \"message\":{\n    \"attachment\":{\n      \"type\":\"video\", \n      \"payload\":{\n        \"attachment_id\": \""+a+"\"\n      }\n    }\n  }\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)