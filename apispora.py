#!/usr/bin/python
#
#
# apispora - a little script to post to diaspora using an
# api, right now only working with pistosapi
# 

this_version= " v0.1.8 alpha"


#
#
#
#



import time, socket, string, sys, httplib, urllib, urllib2, getopt, os


sys.path.append("conf")
sys.path.append("lib")

import users
from pywebfinger import finger
from diaspora_api import *




global debug
debug = "no"


api_version="0" # for /fapi/v0/posts.json

date = time.strftime("%Y-%m-%d - %H:%M", time.localtime(time.time()))

default_txt = "testmessage\n-------------------------\n\napispora-test :: %s \n\n \n\n #federationtestautomated #pistosapi " % date


def api_help():
    
    print """

APISPORA - some tools to post to diaspora via api
           supports right now only pisotsapi 


USAGE 
    %s -x [action] [options]

ACTIONS:

    -x test     -> test a useraccount
                   needs -u 
                   default option; used if not given
                   
    -x patest   -> pistos-api-test
                   needs -u 
                   displays user-info/profile-link, recent notifications
                   and aspects-info
                   (as of 2012-02-24 this is only available 
                   @ diasp0ra.ca)

    -x post     -> post a message to a user@pod.org, 
                   needs -u 
                   

OPTIONS:
    -u usr@pod.org
    
    -a aspect_id -> if you want to post via pistos_api, 
                    you might give an aspect that this post
                    will be linked to
                    can be a list of comma-separated values
                    (as of 2012-02-24 this is only available 
                    @ diasp0ra.ca)
                    
    
    -t "message to send \\n with \\n linebreaks\\n\\n and #hashtags "
        must be more than 5 chars
            
    -l  -> list users

    -d  -> debug ON

CONFIG:
    conf/users.py    -> user-dict

DOC:
    doc/README.apispora

    
    """ % (sys.argv[0])

def pd(debug_input):
    if debug == "yes":
        print "[d] %s " % debug_input

def welcome():
    print """
-----------------------------------------------

APISPORA  

-----------------------------------------------
    
    """
txt = ""
usr_get = ""
action = "test"
uexec = ""
aspect_id = 0
try:
    opts, args = getopt.getopt(sys.argv[1:], "dlhu:t:x:a:")
except getopt.GetoptError, err:
    # print help information and exit:
    print " > ERROR on api / wrong option "
    print str(err) # will print something like "option -a not recognized"
    api_help()
    
    sys.exit(2)

for o, a in opts:

    if o == "-u":
        usr_get = "%s" % a.strip()
    
    elif o == "-t":
        txt = "%s" % a

    elif o == "-a":
        aspect_id = "%s" % a

    elif o == "-x":
        action = "%s" % a.strip()


    elif o == "-d":
        debug = "yes"

    elif o == "-l":
        uexec = "list" 
    else:
        api_help()
        sys.exit()


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        api_help()
        sys.exit(0)




    from diaspora_api import *
    
    if uexec == "list":
        list_users()
        sys.exit()
    
    if usr_get == "":
        print """
[-] ERROR, no user given
    try:    %s -h 
            $s -l


    """ % (sys.argv[0], sys.argv[0])
        sys.exit(2)
    
    if action == "test":

        res = api_test(usr_get)

    elif action == "patest":

        res = papi_test(usr_get)

    elif action == "post":
        if len(txt) < 5:
            txt = default_txt
    
        res = api_post(usr_get, txt)
        if res == 0:
            print "[+] OK posting [ %s ]" % usr_get
    else:
        print """

[-] ERROR - action [ %s ] not found / implemented
    try:    %s -h 
            %s -l


    """ % (action, sys.argv[0], sys.argv[0])
        res = 23
    
    if res == 0:
        sys.exit(0)
    sys.exit(res)

