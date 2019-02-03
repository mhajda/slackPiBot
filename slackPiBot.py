import re
import time
import json
import psutil
from slackclient import SlackClient
import httplib
import base64
import ssl
import json
import urllib
import subprocess

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

#Clear out the existing screen
conn = httplib.HTTPConnection('127.0.0.1', 8080)
headers = {'Accept''': "application/json",
           'Content-Type': "application/json"}

req = conn.request('POST', 'clear', headers=headers)
res = conn.getresponse()
print res.read()

slack_client = SlackClient("YOUR_API_KEY_HERE")

# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "robot-evan":
        slack_user_id = user.get('id')
        break

# Start connection
if slack_client.rtm_connect():
    print "Connected!"

    while True:
        for event in slack_client.rtm_read():
            print "Event received (ALL): %s" % json.dumps(event, indent=2, cls=ComplexEncoder)

            if 'attachments' in event:
                print "Attachments Found"
                for subattachment in event['attachments']:
                    message_text = subattachment['title']
                    print message_text

                    print "Recieved title... sending to screen"

                    req = conn.request('POST', 'clear', headers=headers)
                    res = conn.getresponse()
                    print res.read()

                    req = conn.request('POST', 'show', headers=headers, body=json.dumps({'text':message_text+" "}))
                    res = conn.getresponse()
                    print res.read()

                    req = conn.request('POST', 'autoscroll', headers=headers, body=json.dumps({'is_enabled':'True','interval':'0.1'}))
                    res = conn.getresponse()
                    print res.read()

                    if "unspeakable" in message_text:
                        p = subprocess.Popen(["aplay", "/home/pi/slackPiBot/WhatTheFlip.wav"], stdout=subprocess.PIPE)
                        print p.communicate()

            if 'text' in event and (event['text'].startswith("bot") or event['text'].startswith("Bot")):
                if "Bot" in event['text']:
                    message_text = event['text'].split("Bot")[1]
                else:
                    message_text = event['text'].split("bot")[1]

                print "Bot Message Recieved"

                req = conn.request('POST', 'clear', headers=headers)
                res = conn.getresponse()
                print res.read()

                if "clear" not in message_text:

                    req = conn.request('POST', 'show', headers=headers, body=json.dumps({'text':message_text+" "}))
                    res = conn.getresponse()
                    print res.read()

                    req = conn.request('POST', 'autoscroll', headers=headers, body=json.dumps({'is_enabled':'True','interval':'0.1'}))
                    res = conn.getresponse()
                    print res.read()

                if "what the flip" in message_text:
                    p = subprocess.Popen(["aplay", "/home/pi/slackPiBot/WhatTheFlip.wav"], stdout=subprocess.PIPE)
                    print p.communicate()

        time.sleep(1)
