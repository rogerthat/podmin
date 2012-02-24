#!/usr/bin/python
#
#
#
#

this_version = "v1.0.1 build.666 2011-02-31 "


import getpass, poplib, sys, time, socket, getopt

import subprocess as sub
sys.path.append("conf")
sys.path.append("lib")

from bofh import *

debug = "no"




user = ""
podmin_root_dir = "."
apispora = "%s/apispora.py" % podmin_root_dir



helptext = """

BOFH2API  - a small interface to %s
            post a BOFH_Style excuse to your profile
            version: %s

USAGE:
    email2api.py -u [usr@pod.org]
                    receive mails and post to user-account 
    
    email2api.py -l -> list available users (shortcut to 
                    %s -l
    
    
OPTIONS:
        -d          -> debug ON
                       default: %s

""" % (apispora, this_version, apispora, debug)


i_time = int(time.time())
simulate = "no"


try:
    opts, args = getopt.getopt(sys.argv[1:], "hdlu:")
except getopt.GetoptError, err:
    # print help information and exit:
    print " > ERROR on bofh2api.py / parsing non_existant option " 
    print str(err) # will print something like "option -a not recognized"
    
    print helptext
    
    sys.exit(2)

for o, a in opts:
    
    if o == "-u":
        user = "%s" % a.strip()
    
    elif o == "-l":
        sub.call("%s -l" % apispora, shell=True)
        sys.exit()
    

    elif o == "-d":
        debug = "yes"

    
    else:
        print helptext
        sys.exit()
    


if len(user) < 4:
    print """

[-] ERROR ... no user given; use -u usr@pod.org
              check with -l

-----------------------------------------------------

    """
    print helptext
    sys.exit(2)


excuse = bofh_excuse()
msg = """


###  %s 



#bofh #apipost



""" % excuse

xe = """%s -x post -u %s -t "%s" """ % (apispora, user, msg)
#print xe


try:
    sub.check_call(xe,shell=True)
    print "[+] posted to %s" % user
except:
    print "[-] error while trying to call the api [ %s ] " % xe





