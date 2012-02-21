#!/usr/bin/python
#
#
# email2api - receive mails and post the content
# via apispora to your diaspora-account
#
# v0.1.5
#

debug = "yes"


import getpass, poplib, sys, time, socket, getopt
import email

import subprocess as sub


from email.Parser import Parser

sys.path.append("conf")

from email2api_conf import *


podmin_root_dir = "."
apispora = "%s/apispora.py" % podmin_root_dir


i_time = int(time.time())

max_mails = 300


helptext = """

EMAIL2API - a small interface to %s
            to receive and post messages to diaspora
            from email-accounts
            
            for limits see %s -h


USAGE:
    email2api.py -u [usr@pod.org]
                    receive mails and post to user-account 
    
    email2api.py -l -> list available users (shortcut to 
                    %s -l
                    

""" % (apispora, apispora, apispora)

def getMsgCount():
    # check message count by stat() and list() functions
    numMsgs = M.stat()[0]
    sizeMsgs = M.stat()[1]
    #print "Num msg by stat():", numMsgs
    print "Num msg     :", len(M.list()[1])
    print "Size Inbox  : %s MB" % (sizeMsgs / (1024*1024))
    #print "Most recent:", numMsgs, getSubj(numMsgs)
    return

def getSubj(which):
    # return subject of message with id 'which'
    msg = "\n".join(M.top(which, 1)[1])
    email = parser.parsestr(msg)
    return email.get("Subject")


def print_debug(in_put):
    if debug == "yes":
        try:
            print "[d] %s" % in_put
        except:
            print "[d] ---"
            print in_put

user = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "hlu:")
except getopt.GetoptError, err:
    # print help information and exit:
    print " > ERROR on email2api.pyy / parsing non_existant option " 
    print str(err) # will print something like "option -a not recognized"
    
    print helptext
    
    sys.exit(2)

for o, a in opts:
    
    if o == "-u":
        user = "%s" % a.strip()
    
    elif o == "-l":
        sub.call("%s -l" % apispora, shell=TRUE)
        sys.exit()
    else:
        print helptext
        sys.exit()
    

if len(user) < 4:
    print helptext
    sys.exit(2)

if ssl != "yes":
    M = poplib.POP3(mail_server)
    
else:
    M = poplib.POP3_SSL(mail_server)

M.user(mail_user)
M.pass_(mail_pw)



print_debug(M.stat()[0])
print_debug(M.list()[0])

parser = Parser()


getMsgCount()
numMessages = len(M.list()[1])



new_entries = []
ic = 0

first_date = ""
last_date = ""

for i in range(numMessages):

    processed = i

    if i > max_mails:
        print "[i] MAX_MAILS reached [ %s ] " % max_mails
        break

    for j in M.retr(i+1):
        if type(j) == list: 
            numElements = len(j) 
            outString = "" 
            for k in range(numElements): 
                outString += j[k] 
                outString += '\n' 
            message = email.message_from_string(outString)

            
            
            frm  = message['From'] 
            subj = message['Subject'] 
            date = message['Date']
            if len(first_date) < 1:
                first_date = date
            last_date = date
            msg  = message.get_payload().replace("\"", "'")
            if subj.find(post_identifier) > -1:
                xe = """%s -u %s -t "%s" """ % (apispora, user, msg)
                print_debug(xe)

                try:
                    sub.check_call(xe,shell=True)
                except:
                    print "[-] error while trying to call the api [ %s ] " % xe
                    continue

                if delete_mails == "yes":
                    M.dele(i+1)

                
M.quit()

