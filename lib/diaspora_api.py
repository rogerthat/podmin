#
# functions for diaspora_api
#
# v0.1.16 
#
#

import users
from apispora import *
import xml.etree.ElementTree as ElementTree
import xml.parsers.expat
from xml.dom.minidom import parseString
import tempfile as tmp




tmpdir="/tmp"

def api_test(user):
    #~ try:
        #~ uname = user.split("@")[0].strip()
        #~ uhost = user.split("@")[1].strip()
    #~ except:
        #~ print """
#~ 
#~ [-] ERROR while tying to process user [ %s ]
    #~ must be in the form of: user@pod.org
        #~ 
        #~ """
        #~ return(403)
    #~ 
    #~ pd("checking [ %s ] @ [ %s ] " % (uname, uhost))
    #~ url="/.well-known/host-meta" 
    #~ UA = "Apispora" 
    #~ headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    #~ conn = httplib.HTTPSConnection(uhost, 443, timeout=10)
    #~ if debug == "yes":
        #~ conn.set_debuglevel(9)
    #~ else:
        #~ conn.set_debuglevel(0)
    #~ conn.request("GET", url)
    #~ response = conn.getresponse()
    #~ st, re =  response.status, response.reason
    #~ pd("%s %s" % ( st, re))
    #~ if st != 200:
        #~ return(st)
    #~ data = response.read()
    #~ 
    #~ conn.close()

    print "[+] checking for user: %s" % user
    uinfo = get_user_info(user)
    if uinfo == 0:
        print "[-] ERROR on getting userinfo [ %s ] " % user
        return(1)
    else:
        uprofile = uinfo[0]
        uhcard = uinfo[1]
    
    try:
        i = urllib.urlopen(uprofile).readlines()
        if len(i) > 0:
            upres = "OK "
        else:
            upres = ":: "
    except:
        upres = "ERR"
    
    try:
        i = urllib.urlopen(uhcard).readlines()
        if len(i) > 0:
            ucres = "OK "
        else:
            ucres = ":: "
    except:
        ucres = "ERR"
    
    print """
   Profile  [ %s ] %s
   HCard    [ %s ] %s

    """ % (upres, uprofile, ucres, uhcard)
    
    
    return(0)
def get_user_info(user):
    try:
        wf = finger(user)
        return(wf.profile, wf.hcard)
    except:
        return(0)


def _lese_text(element): 
    typ = element.get("typ", "str") 
    return eval("%s('%s')" % (typ, element.text))




    
def api_post(user, text):

    try:
        usr_key = users.usrs[user].strip()
    except:
        print """

[!] ERROR while trying to check key for user
    [ %s ] 
        
        """ % user
        list_users()
        sys.exit(2)
    pd("api_post :: %s :: %s " % (user, usr_key))

    usr_name = user.split("@")[0].strip()
    usr_host = user.split("@")[1].strip()
    url="/fapi/v%s/posts.json" % (api_version)
    
    params = urllib.urlencode({'token': usr_key, 'text': text})
    pd("sending: %s :: %s ::-> %s " % (user, url, params))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "Apispora %s" % this_version}
    conn = httplib.HTTPSConnection(usr_host, 443, timeout=10)
    if debug == "yes":
        conn.set_debuglevel(9)
    else:
        conn.set_debuglevel(0)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    st, re =  response.status, response.reason
    pd("%s %s" % ( st, re))
    if st != 200:
        return(st)
    data = response.read()
    data
    conn.close()
    return(0)


def list_users():
    
    print """

Listing users

-----------------------------------------------
    """
    
    for user in users.usrs:
        print "  ->  %s "% user

    print """

-----------------------------------------------
    
    """
