#
# basic login-test
#

from selenium import selenium
import time, random, hashlib, sys, unittest, threading, socket


ok_user = []
failed_user = []


class login_check_rc(unittest.TestCase):


    #~ def __init__():
        #~ print local.__dict__
        #~ self.host  = local.__dict__["h"]
        #~ self.user  = local.__dict__["u"]
        #~ self.pw    = local.__dict__["p"]
        #~ self.check_text  = local.__dict__["c"]
        


    def setUp(self):

        self.host  = local.__dict__["h"]
        self.user  = local.__dict__["u"]
        self.pw    = local.__dict__["p"]
        self.check_text  = local.__dict__["c"]
        
        self.verificationErrors = []
        #pd("connecting %s " % self.host)
        self.selenium = selenium("localhost", 4444, "*chrome", "https://%s/" % self.host)
        self.selenium.start(self)
    
    def test_login_rc(self):
        
        u = self.user
        h = self.host
        p = self.pw
        c = self.check_text
        
        #print local.__dict__
        #pd("testing now: [ %s@%s ] " % (u, h))
        sel = self.selenium

        sel.open("/users/sign_in")
        sel.wait_for_page_to_load("30000")
        #~ sel.type("id=user_username", "%s" % u)
        #~ sel.type("id=user_password", "%s" % p)
        #~ sel.click("id=user_submit")
        #~ sel.wait_for_page_to_load("30000")
        #~ sel.open("/stream")
        #~ sel.wait_for_page_to_load("30000")
        #~ try: self.failUnless(sel.is_text_present(""))
        #~ except AssertionError, e: self.verificationErrors.append(str(e))
        #~ self.failUnless(sel.is_text_present("%s" % u))        
        
#~ #        sel.click("link=%s@%s" % (user, host))
#~ #        sel.click("link=Log out")
        #~ sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)


def test_login(u, h, p, c):
    # i know. it's bad style ... but i'm not the threading_global_var_nerd ... 
    global ok_checks
    global failed_user
    global local
    
    local = threading.local()
    local.u = u
    local.h = h
    local.p = p
    local.c = c
    #print local.__dict__
    
    try:
        unittest.main()
    except SystemExit, res:
        res = str(res)
        if res == "False":
            print "[+] OK   %s@%s " % (u, h) 
            ok_user.append("%s@%s" % (u, h))
        else:
            print "[-] ERROR %s@%s :: errno: %s" % (u, h, res ) 
            failed_user.append("%s@%s" % (u, h))
