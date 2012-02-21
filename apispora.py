#!/usr/bin/python
#
#
# apispora - a little script to post to diaspora using an
# api, right now only working with pistosapi
# 

#

import time, socket, string, sys, httplib, urllib, urllib2, getopt, os

sys.path.append("conf")

import users

this_version= " v0.1.4 alpha"

debug = "yes"

api_version="0" # for /fapi/v0/posts.json

date = time.strftime("%Y-%m-%d - %H:%M", time.localtime(time.time()))

default_txt = "testmessage\n-------------------------\n\npistos-api-test :: %s \n\n \n\n #federationtestautomated #pistoapi " % date


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

PISTO_API_POST 

-----------------------------------------------
    
    """

def api_post(user, text):

    try:
        usr_key = users.usrs[usr_get]
    except:
        print """

[!] ERROR while trying to check key for user
    [ %s ] 
        
        """ % usr_get
        list_users()
        sys.exit(2)
    pd("api_post :: %s :: %s " % (usr_get, usr_key))

    usr_name = usr_get.split("@")[0].strip()
    usr_host = usr_get.split("@")[1].strip()
    url="/fapi/v%s/posts.json" % (api_version)
    
    params = urllib.urlencode({'token': usr_key, 'text': txt})
    pd("sending: %s :: %s ::-> %s " % (usr_get, url, params))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(usr_host, 443, timeout=10)
    if debug == "yes":
        conn.set_debuglevel(9)
    else:
        conn.set_debuglevel(9)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    st, re =  response.status, response.reason
    print st, re
    if st != 200:
        return(st)
    data = response.read()
    data
    conn.close()
    return(0)


def pd(debug_input):
    if debug == "yes":
        print "[d] %s " % debug_input

def list_users():
    
    print """

Listing users

-----------------------------------------------
    """
    
    for user in users.usrs:
        print "  ->  %s "% user

    print """

-----------------------------------------------
    
    """

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

