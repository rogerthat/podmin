#
# functions for diaspora_api
#
# v0.1.16 
#
#


from apispora import debug, users, this_version, pistos_api_version, pd
import xml.etree.ElementTree as ElementTree
import xml.parsers.expat
from xml.dom.minidom import parseString
import tempfile as tmp
from pywebfinger import finger

import httplib, urllib, urllib2, time



api_exec = "./apispora.py"


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
        i = urllib2.urlopen(uprofile,timeout=15).readlines()
        #pd(i)
        if len(i) > 0:
            upres = "OK "
        else:
            upres = ":: "
    except:
        upres = "ERR"
    time.sleep(1)
    try:
        i = urllib2.urlopen(uhcard, timeout=15).readlines()
        #pd(i)
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

def papi_test(user):

    try:
        usr_key = users.usrs[user].strip()
    except:
        print """

[!] ERROR while trying to check key for user
    [ %s ] 
        
        """ % user
        list_users()
        sys.exit(2)

    usr_name = user.split("@")[0].strip()
    usr_host = user.split("@")[1].strip()
    api_request = {'token': usr_key}
    params = urllib.urlencode(api_request)
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "Apispora %s" % this_version}
    conn = httplib.HTTPSConnection(usr_host, 443, timeout=10)
    if debug == "yes":
        conn.set_debuglevel(9)
    else:
        conn.set_debuglevel(0)

    url="/fapi/v%s/notifications.json" % (pistos_api_version)
    pd("sending: %s :: %s ::-> %s " % (user, url, params))
    conn.request("GET", url, params, headers)
    try:
        response = conn.getresponse()
    except:
        print "[-] Error in Response to %s " % url
        return(4040)
    st, re =  response.status, response.reason
    pd("%s %s" % ( st, re))
    if st != 200:
        return(st)
    data = response.read()
    print """
---------------------------------------------------
NOTIFICATIONS:

%s


    """ % data

    time.sleep(6)
    url="/fapi/v%s/aspects.json" % (pistos_api_version)
    pd("sending: %s :: %s ::-> %s " % (user, url, params))
    conn.request("GET", url, params, headers)
    try:
        response = conn.getresponse()
    except:
        print "[-] Error in Response to %s " % url
        return(4040)
    st, re =  response.status, response.reason
    pd("%s %s" % ( st, re))
    if st != 200:
        return(st)
    data = response.read()
    dx = data.split("{")
    print """
---------------------------------------------------
ASPECTS:

  ID      - Aspect_Name
----------------------------------
    """ 
    
    for x in dx:
        if x.find("\"name\":") > -1:
            x = x.replace("\"", "")
            xl = x.split(",")
            ntag = xl[0].split(":")[1]
            idtag = xl[4].split(":")[1]
            print " %-6s  -> %s " % (idtag, ntag)
            




    conn.close()
    
#    for entry in data:
#        print entry
    

def get_user_info(user):
    wf = finger(user)
    return(wf.profile, wf.hcard)

    try:
        wf = finger(user)
        return(wf.profile, wf.hcard)
    except:
        return(0)

    
def api_post(user, text, aspect_id):


    try:
        usr_key = users.usrs[user].strip()
    except:
        print """

[!] ERROR while trying to check key for user
    [ %s ] 
        
        """ % user
        list_users()
        sys.exit(2)

    pd("api_post :: %s " % (user))
        

    usr_name = user.split("@")[0].strip()
    usr_host = user.split("@")[1].strip()
    url="/fapi/v%s/posts.json" % (pistos_api_version)

    if aspect_id != 0:
        a_id = aspect_id # " ".join(aspect_id.split(","))
        api_request = {'token': usr_key, 'text': text, "aspect_ids[]" : a_id}
        #~ update( otherDictionary )
        #~ Adds all the key-value pairs from otherDictionary to the current dictionary.
    else:
        api_request = {'token': usr_key, 'text': text}
        
    params = urllib.urlencode(api_request)
    
    pd("sending: %s :: %s ::-> %s " % (user, url, params))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "Apispora %s" % this_version}
    conn = httplib.HTTPSConnection(usr_host, 443, timeout=10)
    if debug == "yes":
        conn.set_debuglevel(9)
    else:
        conn.set_debuglevel(0)
    conn.request("POST", url, params, headers)
    try:
        response = conn.getresponse()
    except:
        print "[-] Error in Response to %s " % url
        return(4040)
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
