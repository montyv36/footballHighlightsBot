# footballHighlightsBot
## What is it
FB messenger bot that will give you the highlights of last night's football matches by messaging [Football_highlights_bot
](https://www.facebook.com/Football_highlights_bot-102830821672521)

## How it works
If you go currently to [Soccer Subreddit](reddit.com/r/soccer) , for every match Users around the world posts snippets of goals / red cards / penalties , basically all the important things that happened in the match. So this bot will go through each of those posts and download those videos , then merge them based on order they're posted and sends it to users. 
The reason why it can be automated even when it's dependent on users posting those videos is that reddit won't go down for some time now and people really need those internet points to feel good about themselves.

## An Example
Let's assume today's date - 24th Nov 2020 and you want to see Liverpool vs Leicester Highlights which occured on 23rd Nov.
Just reply
```bash
team Liverpool
```
Bot will go through reddit posts of last night and most likely fetch these posts - 

[Goal 1](https://www.reddit.com/r/soccer/comments/jz1vg8/liverpool_1_0_leicester_jonny_evans_og_21/)

[Goal 2](https://www.reddit.com/r/soccer/comments/jz28rl/liverpool_2_0_leicester_diogo_jota_41/)

[Handball shout](https://www.reddit.com/r/soccer/comments/jz2xn2/leicester_handball_shout_vs_liverpool_no_penalty/)

[Firmino hits the post](https://www.reddit.com/r/soccer/comments/jz389k/roberto_firmino_hits_the_post_against_leicester/)

[Goal 3](https://www.reddit.com/r/soccer/comments/jz3e8r/liverpool_3_0_leicester_roberto_firmino_86/)

All of these videos will be downloaded and then merged in a single video. After that bot will upload the video in user's chat

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

To Run server on your local - 
```python
python3 bot_server.py
```
