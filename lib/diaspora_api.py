#
# functions for diaspora_api
#
# v0.2.0.24 rc1
#
#

import time, sys

from pywebfinger import finger
import simplejson as json

import httplib, urllib, urllib2, mechanize, cookielib, HTMLParser

from apispora import debug, users, this_version, pistos_api_version, pd
#import xml.etree.ElementTree as ElementTree
#import xml.parsers.expat
#from xml.dom.minidom import parseString
#import tempfile as tmp




api_exec = "./apispora.py"


tmpdir="/tmp"

# src: https://github.com/Pistos/diaspora/wiki/List-of-Pods-Running-This-Code
list_of_pistos_pods = ['diasp0ra.ca', 'calisp0ra.ca', 'c0unt.org', 'diaspora.f4n.de', 'kosmospora.net']

def api_test(user, pw, key):
    """

    call: api_test(user, pw, key)
            set pw/key to 0 it unknown (int(0), not "0")

    this funtction check the webfinger-infos for a given diaspora-user
    and, if pw / api-key are given, checks for new notifications
    and some more tests

    """
    try:
        usr_name = user.split("@")[0].strip()
        usr_host = user.split("@")[1].strip()
    except:
        print "[-] cannot extracte user/host from   %s " % user
    print "[+] checking for user: %s" % user

    uinfo = get_user_info(user)

    res = 0


    if uinfo == 0:
        print "[-] ERROR on getting userinfo [ %s ] " % user
        return(1)
    else:
        uprofile = uinfo[0]
        uhcard = uinfo[1]

    try:
        i = urllib2.urlopen(uprofile,timeout=10).readlines()
        #pd(i)
        if len(i) > 0:
            upres = "OK "
        else:
            upres = ":: "
    except:
        upres = "ERR"
        res += 200
    time.sleep(1)
    try:
        i = urllib2.urlopen(uhcard, timeout=10).readlines()
        #pd(i)
        if len(i) > 0:
            ucres = "OK "
        else:
            ucres = ":: "
    except:
        ucres = "ERR"
        res += 300

    print """
   Profile  [ %s ] %s
   HCard    [ %s ] %s

    """ % (upres, uprofile, ucres, uhcard)


    resa = 0
    if usr_host in list_of_pistos_pods:
        try:
            # incase someone calls with key = "0"
            int(key)
        except:
            pd("checking now pistos-api for %s" % user)
            resa = papi_test(user, key)

    rs = res + resa
    return(rs)

def papi_test(user, usr_key):

    print "--[ testing pistos-api now ]----------------------------------"
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
    dn = json.loads(data)
    print """
---------------------------------------------------
NOTIFICATIONS:
    """
#~ #~

    dn2 = dn["notifications"]
    for idx in dn2:
        for idc in idx:

            print "   - %s   "%   (idc)

    print "\n\n"


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
    dx = json.loads(data)
    print """
---------------------------------------------------
ASPECTS:

  ID      - Aspect_Name
----------------------------------
    """

    dx2 = dx["aspects"]
    for idx in dx2:
        idc = idx["aspect"]
        print "   %5s  - %s" %   (idc["id"], idc["name"])

    print "\n\n"





    conn.close()
    return(0)



def get_user_info(user):
    wf = finger(user)
    return(wf.profile, wf.hcard)

    try:
        wf = finger(user)
        return(wf.profile, wf.hcard)
    except:
        return(0)


def api_post(user, pw, msg, aspect_ids=['public']):
    """
    call: api_post(user, pw, msg, aspect_ids)

        user    : user@pod.org
        pw      : account-pw
        msg     : text as string, can be multilines with markup etc

    this function posts a message for given account,
    emulating a fake api

    set pw/key to 0 it unknown (int(0), not "0")


    """


    pd("api_post :: %s " % (user))


    usr_name = user.split("@")[0].strip()
    usr_host = user.split("@")[1].strip()
    if pw == 0:
        print "[-] ERROR ... empty password"
        return(1000)


    # starting to post -> using login/json via mechanize
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(False)
    br.set_handle_redirect(True)
    br.set_handle_referer(False)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    if debug == "yes":
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('Connection', 'keep-alive'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


    # Open some site, let's pick a random one, the first that pops in mind:
    try:
        r = br.open('https://%s/users/sign_in' % usr_host, timeout=10)
    except mechanize.HTTPError, e:
        print 'ERROR! The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        return(e.code)
    except mechanize.URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        return(404)


    html = r.read()

    csrf = html.split("""csrf-token" content=\"""")[1].split("\"")[0]
    pd("csrf PURE    : %s" % csrf)
    h =  HTMLParser.HTMLParser()
    csrftoken = h.unescape(csrf)
    pd("csrf eascaped: %s" % csrftoken)
    # Show the response headers
    pd(r.info())

    # login
    br.select_form(nr=0)
    # Let's search
    br.form['user[username]']='%s' % usr_name
    br.form['user[password]']='%s' % pw
    br.submit()
    xd = br.response().info()

    # diaspora_cookie
    cookie = xd["set-cookie"].split(";")[0]

    # checking now if i'm logged in (status 200)
    # ok ... not really
    r = br.open('https://%s/stream' % usr_host)
    #pd(r.info())
    html = r.read()
    #print html
    message = {
        'aspect_ids' : aspect_ids,
        "status_message": { 'text': """%s""" % msg},

        #'authenticity_token': csrf,
        }
    pd("cookie: %s" % cookie)
    api_request = json.dumps(message)
    url="/status_messages"

    pd(api_request)
    #params = urllib.urlencode(api_request)
    params = api_request

    pd("sending: %s :: %s ::-> %s " % (user, url, params))
    headers = {"Content-type": "application/json; charset=UTF-8",
                "Connection": "Keep-Alive, keep-alive, TE",
                "User-Agent": "Apispora",
                "Cookie": cookie,
                'X-CSRF-Token': csrftoken,
                }

    time.sleep(1)
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
        sys.exit()
    st, re =  response.status, response.reason
    pd("%s ::: %s" % ( st, re))


    # why is it redirected to /aspects or /?
    if st != 302:
        print "[-] ERROR - status-code (shall be 302): %s" % st
        return(st)
    rloc =  response.getheader('location')
    if rloc.find("/users/sign_in") > -1:
        print "[-] ERROR - redirect_location (shall be / or /aspects): %s" % rloc
        return(2000)
    data = response.read()
    data
    conn.close()

    # logout finally
    r = br.open('https://%s/users/sign_out' % usr_host)

    stream = r.read()



    return(0)



            # old obsolete pistos-code, using now mechanize/json
            # for posts

                #~ url="/fapi/v%s/posts.json" % (pistos_api_version)
            #~
                #~ if aspect_id != 0:
                    #~ a_id = aspect_id # " ".join(aspect_id.split(","))
                    #~ api_request = {'token': usr_key, 'text': text, "aspect_ids[]" : a_id}
                    #~ update( otherDictionary )
                    #~ Adds all the key-value pairs from otherDictionary to the current dictionary.
                #~ else:
                    #~ api_request = {'token': usr_key, 'text': text}
            #~
                #~ params = urllib.urlencode(api_request)
            #~
                #~ pd("sending: %s :: %s ::-> %s " % (user, url, params))
                #~ headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "Apispora %s" % this_version}
                #~ conn = httplib.HTTPSConnection(usr_host, 443, timeout=10)
                #~ if debug == "yes":
                    #~ conn.set_debuglevel(9)
                #~ else:
                    #~ conn.set_debuglevel(0)
                #~ conn.request("POST", url, params, headers)
                #~ try:
                    #~ response = conn.getresponse()
                #~ except:
                    #~ print "[-] Error in Response to %s " % url
                    #~ return(4040)
                #~ st, re =  response.status, response.reason
                #~ pd("%s %s" % ( st, re))
                #~ if st != 200:
                    #~ return(st)
                #~ data = response.read()
                #~ data
                #~ conn.close()



def get_user_dict(uf):
    pd("reading user_list from %s " % uf)


    ud = {}

    fd = open(uf, "r").readlines()

    for line in fd:
        if line[0] == "#":
            continue
        if line.find("::") < 0:
            continue
        user = line.split("::")[0].strip()
        pw   = line.split("::")[1].strip()
        try:
            key = line.split("::")[2].strip()
            if len(key) < 30:
                key = 0
        except:
            key = 0
        pd("    -  %s" % user)
        ud[user] = [pw, key]

    return(ud)

def list_users(uf):

    usrs = get_user_dict(uf)
    if usrs == 0:
        print "nothing found in %s" % uf.split("/")[-1]
    print """

Listing users

-----------------------------------------------
    """

    for user in usrs:
        print "  ->  %s "% user

    print """

-----------------------------------------------

    """

