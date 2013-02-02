#!/usr/bin/env python

# Checks twitter Direct Messages and responds accordingly

import sys, os, twitter, datetime, time, subprocess
from QnA import QnA

consumer_key    = 'HN50b1lMnxGzZZNDspQmRg'
consumer_secret = 'AZdijDvILKj9hlOfjm0aBGN7TaV9pUnB0yw0xiZiI'
access_token    = '5234056420-yvb694iTVagMRf0gV6pBvBuQXwVNgGyponhISXKV'
access_secret   = 'codsfgcBIOzW9hEFSQHaksNiCIXB3oTVGKkprBE1fG1io'
user            = 'user'



def accessTwitter():
    api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)
    return api


def getIP():
   command = 'ifconfig eth0'
   proc    = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
   output  = proc.stdout.read()
   output  = output.splitlines()
   output  = output[1].lstrip(' abcdefghijklmnopqrst:')
   output  = output.partition(' ')
   output  = output[0].lstrip(' abcdefghijklmnopqrst:')
   return output


def getHour():
    now    = datetime.datetime.today()
    hour   = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    second = str(now.second).zfill(2)
    time   = hour + ':' + minute + ':' + second
    return time


def makeMessage(situ, message):

    if situ == 0:
        message = "I""'""m sorry, but I don""'""t understand ""'""" + message + """'"""

    if situ == 1:
        message = 'I switched on. The time is ' + getHour() + '. My IP address is ' + getIP()
    
    elif situ == 2:
        message = 'My program was interrupted by keyboard'
    
    elif situ == 10:
        message = 'My IP is ' + getIP()
    
    elif situ == 11:
        message = 'The time is ' + getHour()
        
    return message
    
    
def initAction():
    # get access to Twitter
    api = accessTwitter()
    
    #construct message to send in direct Tweet
    message = makeMessage(1, None)
    
    # send Tweet
    postMessage(user,message, api)
    
    # checks last ID of last message received
    lastMessageReceived = api.GetDirectMessages()
    lastMessageId = lastMessageReceived[0].id
    return lastMessageId, api
    

def checkForMessage(lastMessageId, api):
    
    lastMessageReceived = api.GetDirectMessages(since_id = lastMessageId)
    
    if len(lastMessageReceived) > 0: 
        message = lastMessageReceived[0].text
        lastMessageId = lastMessageReceived[0].id
        return message, lastMessageId
        
    else: return 0, lastMessageId
    
   
def respondToMessage(message):
    try:
        response = QnA[message]
        if type(response) == int: answer = makeMessage(response, None)
        else: answer = response
    except KeyError: answer = makeMessage(0, message)
    return answer 
    
    
def postMessage(user, message, api):
    message = api.PostDirectMessage(user, message)
    return message


def main():
    
    try:
        # To be performed at boot. Registers with Twitter, and sends tweet with time and IP
        # returns the API and the ID from the last message received
        lastMessageId, api = initAction()
    
        while True: #main loop
            time.sleep(15) # you can only do 350 requests per hour to twitter.
            message, lastMessageId = checkForMessage(lastMessageId, api)
            if(message):
                answer = respondToMessage(message)
                postMessage(user, answer, api)
    
    except (KeyboardInterrupt, SystemExit):
        message = makeMessage(2, None)
        postMessage(user, message, api)
        print "\nKeyboard interrupt. Bye Bye!!"
        

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
