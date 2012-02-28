#
# functions for ftw
#
# v0.0.18
#
#


from ftw import debug, pd, c, conn

from ftw_config import *

import time, random, hashlib, sys, unittest, threading
from selenium import selenium

class login_check_rc(unittest.TestCase):
    global tc
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "https://%s/" % host)
        self.selenium.start()
    
    def test_login_rogerz_rc(self):
        sel = self.selenium
        sel.open("/somepagethatisnthere")
        sel.open("/users/sign_in")
        #~ sel.wait_for_page_to_load("30000")
        #~ sel.type("id=user_username", "%s" % user)
        #~ sel.type("id=user_password", "%s" % pw)
        #~ sel.click("id=user_submit")
        #~ sel.wait_for_page_to_load("30000")
#~ #        try: self.assertEqual("Messages Posted", sel.get_text("%s" % find_text))
#~ #        except AssertionError, e: self.verificationErrors.append(str(e))
        #~ sel.open("/stream")
#~ #        sel.click("link=%s@%s" % (user, host))
#~ #        sel.click("link=Log out")
        #~ sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)


        
        
def start_check(u, h, p, c, testid, start_time):
    # i know. it's bad style ... but i'm not the threading_global_var_nerd ... 
    global user
    global host
    global pw
    global check_text
    global tc
    user = u
    host = h
    pw = p
    check_text = c
    try:
        unittest.main()
    except SystemExit, msg:
        
        tres = str(msg)
        # calculate warning_time here
        if tres == "False":
            c = conn.cursor()
            dbx = "set autocommit=1; update test_results set status = '1' where testid = '%s' and account = '%s@%s'"% (testid, user, host)
            pd(dbx)
            c.execute(dbx)
        else:
            # 
            c = conn.cursor()
            dbx = "set autocommit=1; update test_results set status = '2' where testid = '%s' and account = '%s@%s'"% (testid, user, host)
            pd(dbx)
            c.execute(dbx)
            

        

def exec_scheduler(ud):
    now_time = int(time.time())
    # dont check if older than 24hrs
    oldest = (now_time - (24*60*60))
    dbx = "SELECT tests.testid, tests.ftwinit, schedules.start_time from tests,schedules where tests.testid = schedules.testid and schedules.status = '0' and schedules.start_time < '%s' and tests.init_time > '%s' order by schedules.start_time LIMIT 1;" % (now_time, oldest)
    c.execute(dbx)
    res = c.fetchall()
    if res == ():
        print "[i] no checks found for execution"
        return()
    testid = res[0][0]
    ftwinit = res[0][1]
    start_time = res[0][2]
    dbx = "SELECT account from test_results where testid = '%s' and status != '1' and account != '%s' " % (testid, ftwinit)
    c.execute(dbx)
    accounts = c.fetchall()
    
    for account in accounts:
        account = account[0]
        host = account.split("@")[1]
        user = account.split("@")[0]
        pw = ud[account]
        find_text = ""
        print "[i] checking login for %s " % account
        threads = []
        t = threading.Thread(target=start_check, args=(user, host, pw, find_text, testid, start_time))
        threads.append(t)
        t.start()
        time.sleep(1)
    while len(threading.enumerate()) > 1:
        print "[i] %2s checks running, waiting for threads to finish" % (len(threading.enumerate())-1)
        time.sleep(5)

    dbx = "set autocommit=1; update schedules set status = '1' where testid = '%s' and start_time = '%s'"% (testid, start_time)
    pd(dbx)
    c.execute(dbx)

     
    return(0)

def get_ftw_user_dict():
    pd("reading user_list from %s " % ftw_user_list)
    ud = {}
    
    fd = open(ftw_user_list, "r").readlines()
    
    for line in fd:
        if line[0] == "#":
            continue
        if line.find("::") < 0:
            continue
        user = line.split("::")[0].strip()
        pw   = line.split("::")[0].strip()
        pd("avail user: %s" % user)
        ud[user] = pw
    
    return(ud)

def check_selenium_rc():
    return(0)
    # start-rc when needed?

    # export DISPLAY=:99 && /usr/bin/java -jar /srv/data/selenium_tests/selenium-server-1.0.1/selenium-server.jar -log /srv/data/selenium_tests/logs/selenium.log &






def start_test(ud):
    pd("--[ start-test ]--------------------")
    
    
    if len(ud) < 1:
        print "[-] ERROR ... no users found in user_dict; \n    maybe you need to setup ftw_user_list from ftw_config.py"
        sys.exit(2)
    # selecting a random user
    ul = []
    for u in ud:
        ul.append(u)
    if len(ul) == 0:
        print "\n\n[-] ERROR ... userlist is empty \n\n"
        sys.exit(2)
        
    rc = check_selenium_rc()
    if rc != 0:
        print "\n\n[-] ERROR ... selenium_rc not started \n\n"
        sys.exit(2)
    ftwinit = ul[random.randrange(0,len(ud))]
    init_time = int(time.time())
    hx = "%s-%s-%s" % (time.time(), random.randrange(1,1000000), ftwinit)
    testid = hashlib.sha224(hx).hexdigest() # no maor entropy needed
    pd("testid: %s" % testid)
    
    # creating test-entry
    dbx = """SET autocommit=1; 
    INSERT INTO tests (testid, ftwinit, init_time)
    values ('%s', '%s', '%s');
    
    """ % (testid, ftwinit, init_time)
    

    # creating test-result-defaults
    for u in ul:
        if u == ftwinit:
            continue
        dbx = """%s
    INSERT INTO test_results (testid, account, status)
    values ('%s', '%s', '0');
    """ % (dbx, testid, u)

    # creating scheduler-entries
    
    for val in schedule_time_steps.split(","):
        try:
            s_time = init_time + (int(val.strip()) * 60)
        except:
            continue
        
        dbx = """%s
    -- time-delay: %s min
    INSERT INTO schedules (testid, start_time, status)
    values ('%s', '%s', '0');
    """ % (dbx, val, testid, s_time)
    
    
    c.execute(dbx)
    
    return(testid)
