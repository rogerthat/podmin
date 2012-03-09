#!/usr/bin/python
#
#
# federation-test-warrior
#
# testsuite to test the federation-status among
# diaspora-pods
#
#

this_version = "0.2.0.28"

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
daemon = "no"   # see -D


now_time = int(time.time())
now_date = time.strftime("%Y-%m-%d %H:%M UTC+1", time.localtime(time.time()))


help_text = """

FTW (Federation-Test-Warrior)

ATENCION!!! this is work-in-progress AALPHAA, not all features
            are available, please dont use until it's version 0.2
            GRACIAS!

for more info on usage and setup see
doc/README.ftw / doc/SETUP.ftw

USAGE
    %s -x [action] [options]
    %s -h help

ACTIONS
    -x start-test   -> initializes a tes

    -x scheduler    -> calls scheduler to execute tests

    -x test-logins  -> checks login for every account from
                       ftw_user_list

    -x report       -> status-report

    -x list         -> list upcoming tests

    -x init         -> cleanup db and delete all entries


    -D              -> daemon_mode, will run contiuously 
                       works only on -x scheduler 
                       **

**) not yet, kameraden, not yet!


api     : %s
version : %s

""" % (sys.argv[0], sys.argv[0], api, this_version)


def pd(debug_input):
    if debug == "yes":
        print "[d] %s " % debug_input








# some global-vars



if __name__ == "__main__":

    #thread.start_new_thread(mysql_keepalive, (),)

    if not os.path.isfile(api):
        print """

    ERROR -> api not found :: %s

        """ % api
        sys.exit(2)


    action = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhdx:r:")
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
        elif o == "-D":
            daemon = "yes"
        else:

            print help_text
            print "[i] unknown option [ %s ] " % o
            sys.exit()
    sys.argv = [sys.argv[0]]

    if action == 0:
        print "[i] unknown action [ %s ] " % action
        print help_text
        sys.exit(1)


    rc = check_selenium_rc()
    if rc != 0:
        print "\n\n[-] ERROR [ %s ] ... selenium_rc not started \n\n" % rc
        sys.exit(2)
    else:
        pd("OK Selenium_RemoteControl is up")


    ud = get_ftw_user_dict()
    pd("%s users loaded form user-dict %s " % (len(ud), ftw_user_list))

    if action == "start-test":

        testid = start_test(ud)
        failed = 0
        try:
            int(testid)
            print "\n\n[-] ERROR ... invalid testid \n\n"
            failed = 1
        except:
            print """

[+] OK Test created

        """
        # debug only

    elif action == "scheduler":
        if daemon == "yes":
            while 1:
                print "[i] running scheduler in daemon_mode"
                exec_scheduler(ud)
                time.sleep(10)
        else:
            exec_scheduler(ud)

    elif action == "list":
        list_schedules()

    elif action == "init":
        db_init()

    elif action == "test-logins":
        testid = int(time.time())
        from ftw_test_login import *

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

        rmks = """OK : %s ::
FAILED: %s

        """ % (" ".join(ok_user), " ".join(failed_user))
        dbx = """SET autocommit=1;
    INSERT INTO test_logins (testid, login_ok, ok_bots, login_failed, failed_bots, remarks)
    values ('%s', '%s', '%s', '%s', '%s', '%s');
    """ % (testid, len(ok_user), ", ".join(ok_user), len(failed_user), ", ".join(failed_user), rmks)
        pd(dbx)
        res = db_exec(dbx)
        if res == 0:
            print "[+] db updated with login-test-result"
        else:
            print "[-] ERROR on db_update for login-test-result \n    [ %s ]" % dbres

    elif action == "report":

        test_24h = now_time - (24*60*60)
        print """
> generating results
        """
        dbx = "select login_ok, ok_bots, login_failed, failed_bots, testid from test_logins where testid > '%s' " % test_24h
        tres = db_fetch(dbx)
        try:
            int(res)
            print "[-] ERROR [%s] while trying to get results for report" % res
            sys.exit(2)
        except:
            # we got result, even if emtpy
            pass
        ok_count = 0
        failed_count = 0
        total_count = 0
        for sres in tres:
            print sres
            ok = sres[0]
            failed = sres[2]
            ok_count += int(ok)
            failed_count += int(failed)
        total_count = ok_count + failed_count
        fail_ratio = float(failed_count)/float(total_count)
        if failed_count == 0:
            result = "perfekt"
        elif fail_ratio > login_test_critical_ratio:
            result = "critical"
        elif fail_ratio > login_test_warning_ratio:
            result = "warning"
        else:
            result = "ok"
        out_txt = """
--[ FederationTestWarrior #FTW ]----------------------------------

Login-Test-Result %s

------------------------------------------------------------------

Overall Status      :  %s

Total OK            : %3s
Total FAILED        : %3s
Fail Ratio          : %5s

Testruns    (24hrs) : %3s
Total Tests (24hrs) : %3s

------------------------------------------------------------------

Long result (24hrs)
+------------------------+------+------+--------------------------
| date                   |  OK  | FAIL | RMKS
+------------------------+------+------+--------------------------""" % (now_date, result.upper(), ok_count, failed_count, "%s " % int(fail_ratio*100) + "%" ,len(tres), total_count)
        for res in tres:
            ok = res[0]
            ok_bots = res[1]
            failed = res[2]
            failed_bots = ""
            if int(failed) > 0:
                failed_bots = "FAILED: %s" % res[3].split("@")[1]
            tstamp = time.strftime("%Y-%m-%d %H:%M UTC+1", time.localtime(float(res[4])))

            out_txt =  """%s
| %s | %3s  | %3s  |  %s""" % (out_txt, tstamp, ok, failed, failed_bots)

        out_txt = """%s
+------------------------+------+------+--------------------------
            SUMMARY      | %3s  | %3s  |
                         +------+------+
            """ % (out_txt, ok_count, failed_count)

        print out_txt

    else:
        print """

    [i] Action not yet implemented
        [ %s ]

        """ % action



    print """


    ... exiting

    """

