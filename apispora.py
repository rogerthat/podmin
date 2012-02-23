#!/usr/bin/python
#
#
# apispora - a little script to post to diaspora using an
# api, right now only working with pistosapi
# 

#

import time, socket, string, sys, httplib, urllib, urllib2, getopt, os

sys.path.append("conf")
sys.path.append("lib")

import users
from diaspora_api import *


this_version= " v0.1.4 alpha"

debug = "no"

api_version="0" # for /fapi/v0/posts.json

date = time.strftime("%Y-%m-%d - %H:%M", time.localtime(time.time()))

default_txt = "testmessage\n-------------------------\n\napispora-test :: %s \n\n \n\n #federationtestautomated #pistosapi " % date


def api_help():
    
    print """

APISPORA - some tools to post to diaspora via api
           supports right now only pisotsapi 


USAGE 
    %s [options]

OPTIONS:
    -u usr@pod.org
    
    -t "message to send \\n with \\n linebreaks\\n\\n and #hashtags "
        must be more than 5 chars
            
    -l  -> list users

    -d  -> debug ON

CONFIG:
    conf/users.py    -> user-dict

DOC:
    doc/README.apispora

    
    """ % (sys.argv[0])



def welcome():
    print """
-----------------------------------------------

APISPORA  

-----------------------------------------------
    
    """


def pd(debug_input):
    if debug == "yes":
        print "[d] %s " % debug_input



if __name__ == "__main__":
    if len(sys.argv) < 2:
        api_help()
        sys.exit(0)

    txt = ""
    usr_get = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dlhu:t:")
    except getopt.GetoptError, err:
        # print help information and exit:
        print " > ERROR on api / wrong option "
        print str(err) # will print something like "option -a not recognized"
        api_help()
        
        sys.exit(2)

    for o, a in opts:

        if o == "-u":
            usr_get = "%s" % a
        
        elif o == "-t":
            txt = "%s" % a

        elif o == "-d":
            debug = "yes"

        elif o == "-l":
            list_users()
            sys.exit()
        else:
            api_help()
            sys.exit()


        
    
    if len(txt) < 5:
        txt = default_txt
    
    res = api_post(usr_get, txt)
    
    if res == 0:
        sys.exit(0)
    sys.exit(res)

