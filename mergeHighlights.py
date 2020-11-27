# import praw
import requests
import time
import functools
from moviepy.editor import VideoFileClip, concatenate_videoclips
import urllib
import os
import sys
import cv2
from config import returnConfig
# from praw.models import InlineVideo


high_dict = {}

apiConfig = returnConfig()
file_location = apiConfig.get("storage","filePath")

class HighLights(object):
	list_of_urls = []

	def __init__(self,hig):
		self.list_of_urls = hig

class Goal(object):
	tilte = ""
	url = ""
	team = ""
	time = ""
	ids = ""

	def __init__(self,tilte,url,team,time,ids):
		self.title = title
		self.url = url
		self.team = team
		self.time = time
		self.ids = ids

def make_goal_object(title,url,team,time,ids):
	return Goal(title,url,team,time,ids)

def add_goal(highlight , goal):
	highlight.list_of_urls.append(goal)

def prints(a):
	for x in a.list_of_urls :
		print(x.title +" "+ str(x.time))
	print("---")

def compare_list(a,b):
	a1 = a.time
	b1 = b.time
	# print(a.title+" --- "+str(a1))
	return a1 - b1

def refresh(a):
	start = 0
	finalList = []
	for z in a.list_of_urls:
		time = z.time
		if time - start >= 50:
			finalList.append(z)
		start = time
	a.list_of_urls = finalList


def get(a):
	if a.find("'") == -1 :
		return 0
	x = a.find("'")
	ans = 0
	if valid(a[x-1]) :
		ans = ord(a[x-1]) - 48
		if valid(a[x-2]) :
			ans = (ord(a[x-2]) - 48)*10 + ans
	return ans

def valid(x):
	return ord(x) >= 48 and ord(x) <= 57

def get_video(a,s_id):
	x = requests.get(a)
	v = x.text
	regexText = ""
	if "streamja" in a :
		regexText = ".mp4?secure"
	elif "streamye" in a:
		regexText = "cdn.cdnform"
	elif "streamable" in a:
		regexText = "cdn-cf-east.streamable.com/vid"
	index = v.find(regexText)
	stIndex = index
	enIndex = index
	while stIndex > 0:
		if v[stIndex] != "\"":
			stIndex = stIndex - 1
		else :
			stIndex = stIndex + 1
			break

	while enIndex < len(v):
		if v[enIndex] != "\"":
			enIndex = enIndex + 1
		else :
			break

	videoUrl = v[stIndex : enIndex]
	print(a)
	print(videoUrl)
	if len(videoUrl) == 0:
		print(s_id)
		refreshedUrl = getRefreshedUrl(s_id)
		if len(refreshedUrl) > 0:
			return get_video(refreshedUrl,s_id)
	return videoUrl

def getRefreshedUrl(s_id):
	pushshift_url = "https://api.pushshift.io/reddit/comment/search?subreddit=soccer&link_id="+s_id+"&author=streamablemirrors"
	x = requests.get(pushshift_url).json()
	for z in x["data"]:
		if "streamable.com" in z["body"]:
			start = z["body"].find("streamable.com")
			stIndex = start
			enIndex = start
			while stIndex > 0:
				if z["body"][stIndex] != "(":
					stIndex = stIndex - 1
				else:
					stIndex = stIndex + 1
					break
			while enIndex < len(z["body"]):
				if z["body"][enIndex] != ")":
					enIndex = enIndex + 1
				else:
					break
			return z["body"][stIndex : enIndex]
	return ""


def getMergedVideo(videoUrls , team):
	fileLoc = "/home/montyv36/"
	opener = urllib.request.URLopener()
	opener.addheader('User-Agent', 'whatever')
	start = 1
	height = 728
	width = 410
	for v in videoUrls :
		# print(v)
		location = fileLoc + str(start) + ".mp4"

		opener.retrieve(v , location )
		videoFs = cv2.VideoCapture(location)
		w1 = int(videoFs.get(cv2.CAP_PROP_FRAME_HEIGHT))
		h1 = int(videoFs.get(cv2.CAP_PROP_FRAME_WIDTH))
		if h1 < height :
			height = h1
			width = w1
		start = start + 1

	newStart = 2
	startVideo = fileLoc + "1.mp4"
	print(height)
	print(width)
	while newStart < start:
		location = fileLoc + str(newStart) + ".mp4"
		print("Merging Url - " + location)
		secondVideo = location
		command = "ffmpeg -y -loglevel warning -i "+ startVideo +" -i "file_location+str(newStart)+".mp4 -filter_complex \" [0:v] scale=w=min(iw*"+str(width)+"/ih\\,"+str(height)+"):h=min("+str(width)+"\\,ih*"+str(height)+"/iw), pad=w="+str(height)+":h="+str(width)+":x=("+str(height)+"-iw)/2:y=("+str(width)+"-ih)/2  [video0]; [1:v] scale=w=min(iw*"+str(width)+"/ih\\,"+str(height)+"):h=min("+str(width)+"\\,ih*"+str(height)+"/iw), pad=w="+str(height)+":h="+str(width)+":x=("+str(height)+"-iw)/2:y=("+str(width)+"-ih)/2  [video1];[0:a] anull [audio0];[1:a] anull [audio1];[video0][audio0][video1][audio1] concat=n=2:v=1:a=1 [v][a]\" -map \"[v]\" -map \"[a]\" -c:a aac -c:v h264 -crf 18 -preset veryfast -vsync 2 -f mp4 "+file_location+"mergedVideo.mp4"
		os.system(command)
		os.remove(file_location+"/1.mp4")
		os.rename(file_location+"/mergedVideo.mp4",file_location+"/1.mp4")
		newStart = newStart + 1
	os.rename(file_location+"/1.mp4",file_location+"/mergedVideo.mp4")
	teamFileName = file_location+"/"+team+".mp4"
	command = "ffmpeg -i "+file_location+"/mergedVideo.mp4 -c:v libx264 -crf 24 -b:v 1M -c:a aac "+teamFileName
	os.system(command)
	os.remove(file_location+"/mergedVideo.mp4")
	x = 2
	while x< start:
		if os.path.isfile(file_location+"/"+str(x)+".mp4"):
			os.remove(file_location+str(x)+".mp4")
		x = x+1

teams = []
n = len(sys.argv)
teams.append(sys.argv[1])
submission_id = sys.argv[2]
print("Team - "+sys.argv[1]+" , Sub_id - "+submission_id)

cache = []
for t in teams:
	print(t)
	pushshift_url = "https://api.pushshift.io/reddit/submission/search?q="+t+"&limit=100&sort_type=created_utc&sort=desc&subreddit=soccer&after=6d"
	x = requests.get(pushshift_url).json()
	lists = []
	print(len(x["data"]))
	high_dict[t] = HighLights(lists)
	for z in x["data"]:
		if z["id"] not in cache and ("streamja" in z["url"] or "streamye" in z["url"] or "streamable" in z["url"]) and "[deleted]" not in z["author"]:
			s_id = z["id"]
			url = z["url"]
			title = z["title"]
			cache.append(z["id"])
			goal = make_goal_object(title,url,t,z["created_utc"],s_id)
			add_goal(high_dict[t],goal)

text_body = ""
for key , value in high_dict.items() :
	if len(value.list_of_urls) > 0 and not os.path.isfile(file_location+key+".mp4"):
		text_body = text_body + "**Team Name - "+ key + "** \n\n"
		# print(key)
		videoUrls = []
		prints(value)
		value.list_of_urls.sort(key=functools.cmp_to_key(compare_list))		
		prints(value)
		refresh(value)
		prints(value)
		for f in value.list_of_urls :
			# print(f.title)
			text_body = text_body + "[(" + f.title +")](" + f.url + ")  \n\n"
			videoLink = get_video(f.url,f.ids)
			if len(videoLink) > 0:
				videoUrls.append(videoLink)
		print(videoUrls)
		getMergedVideo(videoUrls , key)
	else:
		print("File already exists")
	command = "python "+file_location+"/fbpost2.py "+key+" "+submission_id
	os.system(command)

print(text_body)