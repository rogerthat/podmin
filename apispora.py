#!/usr/bin/python
#
#
# apispora - a little script to post to diaspora using an
# api, right now only working with pistosapi
#

this_version= " v0.1.99.14 alpha - rc1"

#
#
#
#


import time, socket, string, sys, httplib, urllib, urllib2, getopt, os


sys.path.append("conf")
sys.path.append("lib")

import users, HTMLParser
from pywebfinger import finger

global debug
debug = "no"

pistos_api_version="0" # for /fapi/v0/posts.json

date = time.strftime("%Y-%m-%d - %H:%M", time.localtime(time.time()))

default_txt = "testmessage\n-------------------------\n\napispora-test :: %s \n\n \n\n #federationtestautomated #pistosapi " % date
users_file = "users.list"

def api_help():

    print """

APISPORA - some tools to test diaspora-ccounts or to post to
           diaspora-accounts via api-emulation

ATENCION! ** marked options/actions are **VERY** experimental
            and shall not be used

USAGE
    %s -x [action] [options]

ACTIONS:

    -x test     -> test a useraccount
                   default-action; used if none given
                   needs -u
                   test if account is available and delivers webfinger /
                   hcard-results; if a pistos-api-key is available checks
                   for new notifications and lists aspect_ids

    -x post     -> post a message to a user@pod.org,
                   needs -u and a valid entry in users.list

    -x list     -> list available accounts from users.list

    OBSOLETE (will be executed now on [ -x test ] if valid api-key is found
    -x patest   -> pistos-api-test
                   (as of 2012-02-24 this is only available
                   @ diasp0ra.ca)



OPTIONS:
    -u usr@pod.org  use this account

    -a aspect_id -> if you want to post via pistos_api,
                    you might give an aspect_id that this post
                    will be linked to
                    (as of 2012-02-24 this is only available
                    @ diasp0ra.ca)
                    **
                    default: public, if not given

    -t "message to send with \\n linebreaks\\n\\n  and #hashtags "
        must be more than 5 chars and enclosed with "..."


    -o json      -> export infos from -x test as json **

    -l           -> list users (like -x list))

    -f [file]    -> use [file] as users.list, must be located in conf/

    -d  -> debug ON

CONFIG:
    conf/users.list    -> user/pw/api-key

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
aspect_ids = ['public']

try:
    opts, args = getopt.getopt(sys.argv[1:], "dlhu:t:x:a:f:")
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
        try:
            txt = """
""".join(a.split("\\n"))
        except:
            txt = "%s" % a.strip()
    elif o == "-f":
        users_file = "%s" % a


    elif o == "-a":
        aspect_ids = ['%s'] % a

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

    users_file = "conf/%s" % users_file
    if not os.path.isfile(users_file):
        print "[-] ERROR :: no users_file found :: %s" % users_file
        sys.exit(2)



    from diaspora_api import *

    if uexec == "list" or action == "list":
        pd("reading in users_file %s " % users_file)
        list_users(users_file)
        sys.exit()

    if usr_get == "":
        print """
[-] ERROR, no user given
    try:    %s -h
            $s -l


    """ % (sys.argv[0], sys.argv[0])
        sys.exit(2)


    usrs = get_user_dict(users_file)
    if usrs == 0:
        print "[-] ERROR :: on reading users_file :: %s" % users_file.split("/")[-1]
        sys.exit(2)

    upw = 0
    urs = 0
    uky = 0

    if usr_get in usrs:
        upw = usrs[usr_get][0]
        uky = usrs[usr_get][1]
        usr = usr_get
    else:
        usr = usr_get

    if action == "test":

        res = api_test(usr, upw, uky)

    elif action == "patest":
        # keepo this for comatibilty-reason until 0.4
        res = api_test(usr)

    elif action == "post":
        if len(txt) < 5:
            txt = default_txt

        res = api_post(usr, upw, txt, aspect_ids)
        if res == 0:
            print "[+] OK posting [ %s ]" % usr_get
        else:
            print "[-] ERROR while trying to post to [ %s ]" % usr_get
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

