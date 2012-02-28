#
# functions for ftw
#
# v0.0.20
#
#


from ftw import debug, pd, c, conn

from ftw_config import *

import time, random, hashlib, sys, unittest, threading, socket
from selenium import selenium

class login_check_rc(unittest.TestCase):
    global tc
    
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "https://%s/" % host)
        self.selenium.start()
    
    def test_login_rogerz_rc(self):
        pd("testing now: [ %s@%s ] " % (user, host))
        sel = self.selenium

        sel.open("/users/sign_in")
        #~ sel.wait_for_page_to_load("30000")
        sel.type("id=user_username", "%s" % user)
        sel.type("id=user_password", "%s" % pw)
        sel.click("id=user_submit")
        sel.wait_for_page_to_load("30000")
#~ #        try: self.assertEqual("Messages Posted", sel.get_text("%s" % find_text))
#~ #        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.open("/stream")
#~ #        sel.click("link=%s@%s" % (user, host))
#~ #        sel.click("link=Log out")
        #~ sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)


        
        
def start_check(u, h, p, c, testid, start_time, init_time):
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
    
    nt = int(time.time())
    wt = (int(init_time) + (60*int(warning_time)))
    ct = (int(init_time) + (60*int(critical_time)))

    # debug: make happeningin fail

    check_status = 1
    if nt > ct:
        check_status = 3
    elif nt > wt:
        check_status = 2
    
    try:
        unittest.main()
    except SystemExit, msg:
        
        tres = str(msg)
        # calculate warning_time here
        if tres == "False":
            c = conn.cursor()
            dbx = "set autocommit=1; update test_results set status = '%s', checked = '1' where testid = '%s' and account = '%s@%s'"% (check_status, testid, user, host)
            pd(dbx)
            c.execute(dbx)
        else:
            # 
            outdated_ts = int(schedule_time_steps.split(",")[-1])
            if nt > (int(init_time) + (outdated_ts*60)):
                dbx = "set autocommit=1; update test_results set status = '3', checked = '1'  where testid = '%s' and account = '%s@%s'"% (testid, user, host)
            else:
                dbx = "set autocommit=1; update test_results set status = '2' where testid = '%s' and account = '%s@%s'"% (testid, user, host)
            
            c = conn.cursor()
            pd(dbx)
            c.execute(dbx)
            

        

def exec_scheduler(ud):
    
    
    
    now_time = int(time.time())

    # first, calculate if we're already out of sync
    outdated_ts = int(schedule_time_steps.split(",")[-1])
    outdated_time = (now_time - (outdated_ts * 60) - 1800) # give additional 30 minutes 


    # dont check if older than outdated_timew
    # select only one test at a time
    dbx = "SELECT tests.testid, tests.ftwinit, schedules.start_time, tests.init_time from tests,schedules where tests.testid = schedules.testid and schedules.status = '0' and schedules.start_time < '%s' and schedules.start_time > '%s' order by schedules.start_time LIMIT 1;" % (now_time, outdated_time)
    c.execute(dbx)
    res = c.fetchall()
    if res == ():
        print "[i] no checks found for execution"
        return()
    testid = res[0][0]
    ftwinit = res[0][1]
    start_time = res[0][2]
    init_time = res[0][2]
    
    cst = time.strftime("%F - %H:%M", time.localtime(float(start_time)))
    pd("starting scheduled test %s :: %s " % (cst, testid))
    dbx = "SELECT account from test_results where testid = '%s' and checked != '1' and account != '%s' " % (testid, ftwinit)
    c.execute(dbx)
    accounts = c.fetchall()
    pd("checking %s accounts from selection" % len(accounts))
    if accounts == ():
        print "[i] no accounts found for execution"
    for account in accounts:
        account = account[0]
        host = account.split("@")[1]
        user = account.split("@")[0]
        pw = ud[account]
        find_text = ""
        print "[i] checking login for %s " % account
        threads = []
        t = threading.Thread(target=start_check, args=(user, host, pw, find_text, testid, start_time, init_time))
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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((selenium_server, int(selenium_port)))
        s.close()
        return(0)
    except:
        return(1)
    
    return(2)
    # start-rc when needed?

    # export DISPLAY=:99 && /usr/bin/java -jar lib/selenium-server.jar &






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
        

    ftwinit = ul[random.randrange(0,len(ud))]
    init_time = int(time.time())
    hx = "%s-%s-%s" % (time.time(), random.randrange(1,1000000), ftwinit)
    testid = hashlib.sha224(hx).hexdigest() # no maor entropy needed
    pd("testid  : %s" % testid)
    pd("ftwinit : %s" % ftwinit)
    
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
