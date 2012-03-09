#
# functions for ftw
#
# v0.1.48
#
#


from ftw import debug, pd, now_time, now_date

from ftw_config import *
from diaspora_api import *

import time, random, hashlib, sys, unittest, threading, socket, MySQLdb
from selenium import selenium

from ftw_test_federation_makepost import *
from ftw_test_federation import *



def mysql_keepalive():
    # obsolete
    return()
    #~ while 1:
        #~ pd("mysql_keepalive()")
        #~ cg = conn.cursor()
        #~ cg.execute("select count(id) from tests;")
        #~ r = cg.fetchall()
        #~ time.sleep(5)
        #~ cg.close()

def start_check(user, pw, check_text, testid, start_time, init_time):
    # i know. it's bad style ... but i'm not the threading_global_var_nerd ...

    nt = int(time.time())
    wt = (int(init_time) + (60*int(warning_time)))
    ct = (int(init_time) + (60*int(critical_time)))


    check_status = 1
    if nt > ct:
        check_status = 3
    elif nt > wt:
        check_status = 2

    usr_name = user.split("@")[0].strip()
    usr_host = user.split("@")[1].strip()
    if pw == 0:
        print "[-] ERROR ... empty password"
        return(1000)


    nt = int(time.time())
    wt = (int(init_time) + (60*int(warning_time)))
    ct = (int(init_time) + (60*int(critical_time)))

    # looks like mechanize dioesnt werk with displaying the stream???
    #~ # starting to post -> using login/json via mechanize
    #~ br = mechanize.Browser()
#~
    #~ # Cookie Jar
    #~ cj = cookielib.LWPCookieJar()
    #~ br.set_cookiejar(cj)
#~
    #~ # Browser options
    #~ br.set_handle_equiv(True)
    #~ br.set_handle_gzip(False)
    #~ br.set_handle_redirect(True)
    #~ br.set_handle_referer(False)
    #~ br.set_handle_robots(False)
#~
    #~ # Follows refresh 0 but not hangs on refresh > 0
    #~ br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#~
    #~ # Want debugging messages?
    #~ if debug == "yes":
        #~ br.set_debug_http(True)
        #~ br.set_debug_redirects(True)
        #~ br.set_debug_responses(True)
#~
    #~ # User-Agent (this is cheating, ok?)
    #~ br.addheaders = [('Connection', 'keep-alive'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#~
#~
    #~ # Open some site, let's pick a random one, the first that pops in mind:
    #~ try:
        #~ r = br.open('https://%s/users/sign_in' % usr_host, timeout=10)
    #~ except mechanize.HTTPError, e:
        #~ print 'ERROR! The server couldn\'t fulfill the request.'
        #~ print 'Error code: ', e.code
        #~ return(e.code)
    #~ except mechanize.URLError, e:
        #~ print 'We failed to reach a server.'
        #~ print 'Reason: ', e.reason
        #~ return(404)
#~
#~
    #~ html = r.read()
#~
    #~ pd(r.info())
#~
    #~ csrf = html.split("""csrf-token" content=\"""")[1].split("\"")[0]
    #~ pd("csrf PURE    : %s" % csrf)
    #~ h =  HTMLParser.HTMLParser()
    #~ csrftoken = h.unescape(csrf)
    #~ pd("csrf eascaped: %s" % csrftoken)
    #~ # Show the response headers
#~
#~
    #~ # login
    #~ br.select_form(nr=0)
    #~ # Let's search
    #~ br.form['user[username]']='%s' % usr_name
    #~ br.form['user[password]']='%s' % pw
    #~ br.submit()
    #~ xd = br.response().info()
#~
    #~ # diaspora_cookie
    #~ cookie = xd["set-cookie"].split(";")[0]
#~
    #~ # checking now tag #federationtesautomated
    #~ r = br.open('https://%s/%s' % (usr_host, check_tag))
    #pd(r.info())

    #~ ## debug only
    #~ stream = r.read(100000)
    #~ print stream
    #~ raw_input("> %s should find: %s \n> [enter] ::" % (user, testid))
    #~
    #~ ##
    #~


    # making some default
    dbx = "set autocommit=1;"

    tres = ftw_check(usr_name, usr_host, pw, check_text)
    check_txt = check_text[0:10]
    if tres == 0:

        print "[+] OK!! %s successfully found %s" % (user, check_txt)
        dbx = "set autocommit=1; update test_results set status = '%s', checked = '1', checked_time = '%s' where testid = '%s' and account = '%s'"% (check_status, nt, testid, user)
    else:
        #
        outdated_ts = int(schedule_time_steps.split(",")[-1])
        if nt > (int(init_time) + (outdated_ts*60)):
            dbx = "set autocommit=1; update test_results set status = '4', checked = '1'  where testid = '%s' and account = '%s'"% (testid, user)


    pd(dbx)
    res = db_exec(dbx)
    if res != 0:
        print "[-] ERROR on db-insert %s " % dbx
    return(0)


def db_exec(dbx):
    # due to http://stackoverflow.com/questions/567622/is-there-a-pythonic-way-to-try-something-up-to-a-maximum-number-of-times
    # issue raised during livetests
    #

    try:
        conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass,db=db_db )
        pd("DB::starting db_connection (db-init)")

    except:
        print "[-]ERROR DB::db-connection-error (db-init)"
        sys.exit(2)

    attempts = 0
    error = 40404
    while attempts < 5:
        try:
            cx = conn.cursor()
            cx.execute(dbx)
            cx.close()
            conn.close()
            return(0)
        except MySQLdb.Error, e:
            error = "MySQL Error %d: %s" % (e.args[0], e.args[1])
            attempts += 1
            print "try: %s" % attempts
            print error
            time.sleep(0.1)
            error = e.args[0]
    conn.close()
    return(error)


def db_fetch(dbx):

    try:
        conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass,db=db_db )
        pd("DB::starting db_connection (db-init)")

    except:
        print "[-]ERROR DB::db-connection-error (db-init)"
        sys.exit(2)

    attempts = 0
    error = 50505
    while attempts < 5:
        try:
            cx = conn.cursor()
            cx.execute(dbx)
            res = cx.fetchall()
            conn.close()

            return(res)
        except MySQLdb.Error, e:
            error = "MySQL Error %d: %s" % (e.args[0], e.args[1])
            attempts += 1
            print "try: %s" % attempts
            print error
            time.sleep(0.1)
            error = e.args[0]
    conn.close()
    return(error)


def list_schedules():

    now_time = int(time.time())

    outdated = now_time - (24*60*60)

    now_time = int(time.time())
    dbx = "SELECT tests.testid, tests.ftwinit, schedules.start_time, tests.init_time from tests,schedules where tests.testid = schedules.testid and schedules.status = '0' and schedules.start_time > '%s' and schedules.start_time < '%s'  order by schedules.start_time;" % (outdated, now_time)

    ress = db_fetch(dbx)
    try:
        int(res)
        print "[-] ERROR [%s] while trying to get results for scheduler" % res
        return(res)
    except:
        # we got result, even if emtpy
        pass
    print """
> due_time reached ( %s tests found) 
    """ % len(ress)
    for st in ress:
        testid = st[0]
        testid =  testid[0:6]
        ftwinit = st[1]
        start_time = st[2]
        init_time = st[3]
        time_till_run = ((int(start_time) - int(now_time)) / 60) + 1
        start_date = time.strftime("%H:%M", time.localtime(float(start_time)))
        init_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(init_time)))
        print """
--[ %15s ]-------------------------------------------

TestID          : %s
Test Started    : %s
Due_Time        : %s
Overdue         : %s minutes
        """ % (ftwinit, testid, init_date, start_date, time_till_run,  )



    print """
> upcoming events
    """

    dbx = "SELECT tests.testid, tests.ftwinit, schedules.start_time, tests.init_time from tests,schedules where tests.testid = schedules.testid and schedules.status = '0' and schedules.start_time > '%s' order by schedules.start_time LIMIT 5;" % (now_time)

    ress = db_fetch(dbx)

    try:
        int(res)
        print "[-] ERROR [%s] while trying to get results for scheduler" % res
        return(res)
    except:
        # we got result, even if emtpy
        pass
    print "[i] next 5 Tests: "
    for st in ress:
        testid = st[0]
        testid =  testid[0:6]
        ftwinit = st[1]
        start_time = st[2]
        init_time = st[3]
        time_till_run = ((int(start_time) - int(now_time)) / 60) + 1
        start_date = time.strftime("%H:%M", time.localtime(float(start_time)))
        init_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(init_time)))
        print """
--[ %15s ]-------------------------------------------

TestID          : %s
Test Started    : %s
Next Run        : %s
Time Left       : %s minutes
        """ % (ftwinit, testid, init_date, start_date, time_till_run,  )


def db_init():
    print "\n\n\n[!] DB-INIT \n\n\n"
    tables = ["tests", "schedules", "test_results", "test_logins" ]

    say_ok = raw_input("> type 'OK' if you really want to reset your test_db \n> ")
    if say_ok != "OK":
        print " ... nothign to do here"
        return()
    print """
    """
    for table in tables:
        dbx = "set autocommit=1; delete from %s; " % table
        res = db_exec(dbx)
        if res == 0:
            print " [+] purged table %s" % table
        else:
            print "[-] ERROR [ %s ] while purging table %s" % (res, table)

    return()


def exec_scheduler(ud):



    now_time = int(time.time())

    # first, calculate if we're already out of sync
    outdated_ts = int(schedule_time_steps.split(",")[-1])
    outdated_time = (now_time - (outdated_ts * 60) - 1800) # give additional 30 minutes


    # dont check if older than outdated_timew
    # select only one test at a time
    dbx = "SELECT tests.testid, tests.ftwinit, schedules.start_time, tests.init_time from tests,schedules where tests.testid = schedules.testid and schedules.status = '0' and schedules.start_time < '%s' and schedules.start_time > '%s' order by schedules.start_time LIMIT 5;" % (now_time, outdated_time)

    res = db_fetch(dbx)

    try:
        int(res)
        print "[-] ERROR [%s] while trying to get results for scheduler" % res
        return(res)
    except:
        # we got result, even if emtpy
        pass

    if res == ():
        print "[i] no checks found for execution"

        list_schedules()



    for xt in res:
        testid = xt[0]
        testid_txt = testid[0:6]
        ftwinit = xt[1]
        start_time = xt[2]
        init_time = xt[3]

        cst = time.strftime("%F - %H:%M", time.localtime(float(start_time)))
        pd("starting scheduled test %s :: %s " % (cst, testid_txt))
        print "[i] starting check for %s :: %s \n    init_date: %s" % (ftwinit, testid_txt, time.strftime("%H:%M", time.localtime(float(init_time)))
)
        
        ##debug
        
        dbx = "SELECT account from test_results where testid = '%s' and checked != '1'" % (testid)
        
        dbx = "SELECT account from test_results where testid = '%s' and checked != '1' and account != '%s' " % (testid, ftwinit)
#        dbx = "SELECT account from test_results where testid = '%s' and checked != '1' and account != '%s' " % (testid, ftwinit)
        res = db_fetch(dbx)

        try:
            int(res)
            print "[-] ERROR [%s] while trying to get results for scheduler" % res
            return(res)
        except:
            # we got result, even if emtpy
            pass
        accounts = res
        print "[i] checking %s accounts from selection" % len(accounts)
        if accounts == ():
            print "[i] no accounts found for execution"
        for account in accounts:
            account = account[0]
            host = account.split("@")[1]
            user = account.split("@")[0]
            try:
                pw = ud[account]
            except:
                print "[-] ERROR ... cannot find pw for %s " % account
                continue
            threads = []

            find_text = "ftw.%s" % testid[0:12].strip()
            print "[i] checking #ftw [ %s ] for %s " % (find_text, account)
            ##debug
            #find_text = "ftw"
            try:
                t = threading.Thread(target=start_check, args=(account, pw, find_text, testid, start_time, init_time))
                threads.append(t)
                t.start()
                time.sleep(int(ramp_up_delay))
            except:
                print "thread-exeption"
                time.sleep(3)
                start_check(account, pw, find_text, testid, start_time, init_time)

        max_runtime = 90 # seconds
        while len(threading.enumerate()) > 1:
            xt = int(time.time())
            if xt - now_time > max_runtime:
                t.join()
                break
            print "[i] %2s checks running, waiting for threads to finish" % (len(threading.enumerate())-1)
            time.sleep(5)

        #~ # debug - keep alive 3 min to see if mysql stays open
        #~ print "debug-sleeping"
        #~ time.sleep(120)


        dbx = "set autocommit=1; update schedules set status = '1' where testid = '%s' and start_time = '%s'"% (testid, start_time)
        res = db_exec(dbx)
        if res != 0:
            print "[-] ERROR [ %s ] while trying to update scheduler-table" % res
            pd(dbx)
        else:
            print "[+] run finished %s :: %s " % (ftwinit, testid_txt)
        time.sleep(0.1)



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
        pw   = line.split("::")[1].strip()
        pd("    -  %s" % user)
        ud[user] = pw

    return(ud)

def check_selenium_rc():

    # obsolete NOT

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
    testid = hashlib.sha224(hx).hexdigest() # no more entropy needed
    pd("testid  : %s" % testid)
    pd("ftwinit : %s" % ftwinit)

    pw = ud[ftwinit]
    usr_name = ftwinit.split("@")[0].strip()
    usr_host = ftwinit.split("@")[1].strip()
    msg = """
##### federation-test %s
----------------------------------------
automated test-entry @ %s

testid: ftw.%s
date: %s
timestamp: %s
botlink: https://%s/u/%s


#federationtestwarriors #federationtestautomated



    """ % (now_date, ftwinit, testid, now_date, now_time, usr_host, usr_name)


    pd("posting now -> %s " % ftwinit)
    res = api_post(ftwinit, pw, msg)
    if res != 0:
        print "[-] ERROR while trying to create test-post @ %s " % ftwinit
        return(3000)

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

    res = db_exec(dbx)
    if res != 0:
        print "[-] ERROR [ %s ] while trying to create test + scheduler-entries" % res
        pd(dbx)
    else:
        print "[+] OK Test created  %s :: %s " % (ftwinit, testid)
    print msg


    return(testid)
