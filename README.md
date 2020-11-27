# footballHighlightsBot
## What is it
FB messenger bot that will give you the highlights of last night's football matches by messaging [Football_highlights_bot
](https://www.facebook.com/Football_highlights_bot-102830821672521)

## How it works
If you go currently to [Soccer Subreddit](reddit.com/r/soccer) , for every match Users around the world posts snippets of goals / red cards / penalties , basically all the important things that happened in the match. So this bot will go through each of those posts and download those videos , then merge them based on order they're posted and sends it to users. 
The reason why it can be automated even when it's dependent on users posting those videos is that reddit won't go down for some time now and people really need those internet points to feel good about themselves.

## Setup
```python
pip3 install -r requirements.txt
```

Edit this file - config.ini
```python
[storage]
filePath = /Users/verma.shubham/Documents/ #location where you will store videos

[api_keys]
fb_page_access_token = $ACCESS_TOKEN  #Access token for your FB app
fb_page_verify_token = $VERIFY_TOKEN #Verify token for verification with facebook developer app
football_api_key = $FOOTBALL_API_KEY #To support "show fixtures" command for bot
```
