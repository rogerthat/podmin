#
# functions for diaspora_api
#



def api_post(user, text):

    try:
        usr_key = users.usrs[usr_get]
    except:
        print """

[!] ERROR while trying to check key for user
    [ %s ] 
        
        """ % usr_get
        list_users()
        sys.exit(2)
    pd("api_post :: %s :: %s " % (usr_get, usr_key))

    usr_name = usr_get.split("@")[0].strip()
    usr_host = usr_get.split("@")[1].strip()
    url="/fapi/v%s/posts.json" % (api_version)
    
    params = urllib.urlencode({'token': usr_key, 'text': txt})
    pd("sending: %s :: %s ::-> %s " % (usr_get, url, params))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
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
