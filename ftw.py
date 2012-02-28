#!/usr/bin/python
#
#
# federation-test-warrior 
#
# testsuite to test the federation-status among 
# diaspora-pods
#
#

this_version = "0.1.0"

import MySQLdb, time, os, sys, getopt
import subprocess as sub
import unittest, thread, threading

sys.path.append("conf")
sys.path.append("lib")

from diaspora_api import get_user_info, api_exec
from ftw_config import *
from ftw_func import *


api = api_exec

debug = "yes"

help_text = """

FTW (Federation-Test-Warrior)

ATENCION!!! this is work-in-progress, not all features
            are available, please dont use until it's version 0.2
            GRACIAS!

for more info on usage and setup see
doc/README.ftw / doc/SETUP.ftw

USAGE
    %s -x [action] [options]
    %s -h help

ACTIONS
    -x start-test   -> starts a test-init 
    -x scheduler    -> calls scheduler to execute tests 
    -x test-logins  -> checks login for every account from 
                       ftw_user_list
**  -x list         -> list running/unfinished tests
**  -x cleanup      -> closes unfinished tests > close_final_time
**  -x report       -> interactive status-report
   
**) not yet, kameraden, not yet!
    

api: %s 

""" % (sys.argv[0], sys.argv[0], api)


def pd(debug_input):
    if debug == "yes":
        print "[d] %s " % debug_input





pd("DB::starting db_connection (db-init)")
try:
    conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass,db=db_db )
    c = conn.cursor()

except:
    print "[-]ERROR DB::db-connection-error (db-init)"
    sys.exit(2)


# some global-vars



if __name__ == "__main__":
    
    if not os.path.isfile(api):
        print """
    
    ERROR -> api not found :: %s 
        
        """ % api
        sys.exit(2)
        
    
    action = 0
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdx:r:")
    except getopt.GetoptError, err:
        # print help information and exit:
        print " > ERROR on ftw / wrong option "
        print str(err) # will print something like "option -a not recognized"
        print help_text
        
        sys.exit(2)
    
    
    for o, a in opts:
        if o == "-x":
            action = "%s" % a.strip()
        elif o == "-d":
            debug = "yes"
        else:
            
            print help_text
            print "[i] unknown option [ %s ] " % o
            sys.exit()
    sys.argv = [sys.argv[0]]
    
    if action == 0:
        print "[i] unknown action [ %s ] " % action
        print help_text
        sys.exit()
    
    
    rc = check_selenium_rc()
    if rc != 0:
        print "\n\n[-] ERROR [ %s ] ... selenium_rc not started \n\n" % rc
        sys.exit(2)
    else:
        pd("OK Selenium_RemoteComntrol is up")
    
    
    ud = get_ftw_user_dict()
    pd("%s users loaded form user-dict %s " % (len(ud), ftw_user_list))
    
    if action == "start-test":
        
        testid = start_test(ud)
        if testid == 0:
            print "\n\n[-] ERROR ... invalid testid \n\n"
            sys.exit(2)
        # debug only
    
    elif action == "scheduler":
        exec_scheduler(ud)
        

    elif action == "test-logins":
        print "\n----------------------- \n> testing logins \n"


        



        for u in ud:
            host = u.split("@")[1]
            user = u.split("@")[0]
            pw = ud[u]
            find_text = ""
            print "[i] checking login for %s " % u
            threads = []
            t = threading.Thread(target=test_login, args=(user, host, pw, find_text))
            threads.append(t)
            t.start()
            time.sleep(int(ramp_up_delay))
        if debug == "yes":
            time.sleep(1)
        else:
            time.sleep(15)
        while len(threading.enumerate()) > 1:
            print "[i] %2s checks running, waiting for threads to finish" % (len(threading.enumerate())-1)
            time.sleep(3)
        
        print "\n--[ Login-Test-Results ]----------------------------------------------\n"

        if len(ok_user) == len(ud):
            print "[+] All logins OK [ %s / %s ] " % (len(ok_user), len(ud))
        else:
            print "[-] Failed logins [ %s / %s ] " % (len(failed_user), len(ud))
            for fu in failed_user:
                print "   - %s " % fu
            
        
    else:
        print """
    
    [i] Action not yet implemented
        [ %s ] 
        
        """ % action
    
        
    c.close()
    
    
    print """
    
    
    ... exiting
    
    """
    
