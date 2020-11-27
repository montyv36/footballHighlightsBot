import requests
import json
from datetime import datetime, timedelta
import os
import sys
import random
from config import returnConfig


apiConfig = returnConfig()
file_location = apiConfig.get("storage","filePath")
fb_page_access_token = apiConfig.get("api_keys","fb_page_access_token")
football_api_key = apiConfig.get("api_keys","football_api_key")

rec_id = sys.argv[1]
x = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
y = (datetime.today() - timedelta(2)).strftime('%Y-%m-%d')
message1 = "Popular Matches yesterday"
filePath = file_location + y + ".json"
a = {}
regex = "(* U *)"

def writeInFile(a,filePath):
	file = open(filePath,"w")
	for v in a:
		homeTeam = v["match_hometeam_name"]
		awayTeam = v["match_awayteam_name"]
		line = homeTeam + regex + awayTeam +"\n"
		file.write(line)
	file.close()


if not os.path.isfile(filePath):
	print("Cache Miss")
	response = requests.request("GET","https://apiv2.apifootball.com/?action=get_events&from="+y+"&to="+x+"&APIkey="+football_api_key)	
	a = response.json()
	writeInFile(a,filePath)


print("Cache Hit")
fixtures = []
file = open(filePath,'r')
lines = file.readlines()
for ll in lines:
	x = ll.split(regex)[0]
	y = ll.split(regex)[1]
	y = y[0:len(y) - 1]
	fixtures.append((x,y))


popularTeams = {}
popularTeams["Bayern Munich"] = "Bayern"
popularTeams["Liverpool"] = "Liverpool"
popularTeams["Manchester City"] = "Manchester+City"
popularTeams["Paris SG"] = "Paris"
popularTeams["Barcelona"] = "Barcelona"
popularTeams["Real Madrid"] = "Real+Madrid"
popularTeams["Dortmund"] = "Dortmund"
popularTeams["Chelsea"] = "Chelsea"
popularTeams["Arsenal"] = "Arsenal"
popularTeams["Tottenham"] = "Tottenham"
popularTeams["Juventus"] = "Juventus"
popularTeams["AC Milan"] = "Milan"
popularTeams["Inter"] = "Inter"
popularTeams["Manchester Utd"] = "United"
popularTeams["Atl. Madrid"] = "Inter"

buttons = []
for v in fixtures:
	homeTeam = v[0]
	awayTeam = v[1]
	if homeTeam in popularTeams :
		button = {}
		button["type"] = "postback"
		button["title"] = homeTeam + " vs " + awayTeam
		button["payload"] = popularTeams[homeTeam]
		buttons.append(button)
	elif awayTeam in popularTeams :
		button = {}
		button["type"] = "postback"
		button["title"] = homeTeam + " vs " + awayTeam
		button["payload"] = popularTeams[awayTeam]
		buttons.append(button)


data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient' : json.dumps({
        		'id' : rec_id
        	}),
        'message': json.dumps({
            'attachment': {
                'type': 'template',
                'payload': {
                	'template_type' : 'button',
                	'text' : 'Yesterday\'s fixtures !',
                	'buttons' : buttons
                }
            }
        })
    }
print(buttons)

if len(buttons) > 0:
	s = 0
	while(len(buttons[s:s+3])>0):
		butsi = buttons[s:s+3]
		messageText = "More fixtures "
		if s==0:
			messageText = "Yesterday\'s fixtures !"
		data = {
	        # encode nested json to avoid errors during multipart encoding process
	        'recipient' : json.dumps({
	        		'id' : rec_id
	        	}),
	        'message': json.dumps({
	            'attachment': {
	                'type': 'template',
	                'payload': {
	                	'template_type' : 'button',
	                	'text' : messageText,
	                	'buttons' : butsi
	                }
	            }
	        })
	    }

		url = "https://graph.facebook.com/v2.6/me/messages?access_token="+fb_page_access_token
		# payload = "{\n  \"recipient\":{\n    \"id\":\""+rec_id+"\"\n  },\n  \"message\":{\n    \"attachment\":{\n      \"type\":\"template\",\n      \"payload\":{\n        \"template_type\":\"button\",\n        \"text\":\"Yesterday's fixtures !\",\n        \"buttons\":"+str(json.dumps(buttons))+"\n      }\n    }\n  }\n}"
		print(data)
		headers = {
		  'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data = data,verify = False)
		s = s+ 3
else :
	url = "https://graph.facebook.com/v2.6/me/messages?access_token="+fb_page_access_token
	payload = "{\n  \"recipient\":{\n    \"id\":\""+sub_id+"\"\n  },\n  \"message\":{\n    \"text\": \"Error , Couldn't generate video !!\"  }\n}"
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data = payload)