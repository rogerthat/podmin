#!/usr/bin/python
#
#
# email2api - receive mails and post the content
# via apispora to your diaspora-account
#
#

this_version = "v0.1.8"


import getpass, poplib, sys, time, socket, getopt
import email

import subprocess as sub


from email.Parser import Parser

sys.path.append("conf")

from email2api_conf import *


debug = "no"


def getMsgCount():
    # check message count by stat() and list() functions
    numMsgs = M.stat()[0]
    sizeMsgs = M.stat()[1]
    #print "Num msg by stat():", numMsgs
    print_debug("Num msg     : %s" % len(M.list()[1]))
    print_debug("Size Inbox  : %s MB" % (sizeMsgs / (1024*1024)))
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
podmin_root_dir = "."
apispora = "%s/apispora.py" % podmin_root_dir



helptext = """

EMAIL2API - a small interface to %s
            to receive and post messages to diaspora
            from email-accounts
            version: %s

USAGE:
    email2api.py -u [usr@pod.org]
                    receive mails and post to user-account 
    
    email2api.py -l -> list available users (shortcut to 
                    %s -l
    
    email2api.py -s -> select user via email_subject
    
    email2api.py -c -> check, how many emails are in the queue
    
OPTIONS:
        -d          -> debug ON
                       default: %s
        -n          -> just simulate (no posting/no deletion of mails)

""" % (this_version, apispora, apispora, debug)


i_time = int(time.time())
simulate = "no"
check_only = "no"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hdcnlsu:")
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
        sub.call("%s -l" % apispora, shell=True)
        sys.exit()
    
    elif o == "-s":
        user = "subjectselect"    

    elif o == "-d":
        debug = "yes"

    elif o == "-c":
        check_only = "yes"


    elif o == "-n":
        simulate = "yes"
    
    else:
        print helptext
        sys.exit()
    

parser = Parser()

if ssl != "yes":
    M = poplib.POP3(mail_server)
    
else:
    M = poplib.POP3_SSL(mail_server)

M.user(mail_user)
M.pass_(mail_pw)


numMessages = len(M.list()[1])
    

if check_only == "yes":
    debug = "yes"
    getMsgCount()
    sys.exit()

if len(user) < 4:
    print """

[-] ERROR ... no user given; use -u usr@pod.org
              or -s to select via mail_subject

-----------------------------------------------------

    """
    print helptext
    sys.exit(2)



getMsgCount()


ic = 0


for i in range(numMessages):

    processed = i

    if i > int(max_mails):
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
            msg  = message.get_payload().replace("\"", "'")
            if subj.find(post_identifier) > -1:
                print_debug(" OK - valid identifier found in subject [ %s ]" % subj)
                try:
                    # in case the footer is corrupt
                    msg = "%s \n%s" % (msg, mail_footer)
                except:
                    pass
                if user == "subjectselect":
                    try:
                        user = subj.split(post_identifier)[1].strip()
                    except:
                        print """[-] ERROR while trying to identify user in subjetc [ %s ] """ % subj
                        continue
                xe = """%s -x post -u %s -t "%s" """ % (apispora, user, msg)
                print_debug(xe)


                if simulate == "no":
                    try:
                        sub.check_call(xe,shell=True)
                        print "[+] posted to %s" % user
                    except:
                        print "[-] error while trying to call the api [ %s ] " % xe
                        continue

                    if delete_mails == "yes":
                        M.dele(i+1)
                else:
                    print "[s] simulated posting to [ %s ]" % user
            else:
                print "[i] ?? no valid identifier found in subject [ %s ] ... deleting " % subj
                
                if simulate == "no":
                    if delete_invalid_mails == "yes":
                        M.dele(i+1)
            time.sleep(6)
                
M.quit()

