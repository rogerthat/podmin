#!/usr/bin/python
#
#
# get stuff from the stream an post to apispora
#
# please note, this needs a db that is not yet 
# public available
#


import MySQLdb, time, os
import subprocess as sub

from apispora import *

from rdf_config import *

api = "./apispora.py"
bot = ""
action = "no"
providers = ["all"]


helP = """

post_rdf 

options:
    -l list available rdf-providers
    -p p1,p2,p3
     provider1,provider2,provider3
    -u user to post to (see %s -l)


""" % (api)



if not os.path.isfile(api):
    print """

ERROR -> api not found :: %s 
    
    """ % api
    sys.exit(2)
    


try:
    opts, args = getopt.getopt(sys.argv[1:], "hlp:u:")
except getopt.GetoptError, err:
    # print help information and exit:
    print " > ERROR on api / wrong option "
    print str(err) # will print something like "option -a not recognized"
    print helP
    
    sys.exit(2)


for o, a in opts:
    if o == "-p":
        px = "%s" % a
        if px == "all":
            providers = ["all"]
        else:
            providers = ("%s" % a).split(",")

    elif o == "-l":
        action = "show"

    elif o == "-u":
        bot = "%s" % a


    else:
        print helP
        sys.exit()


try:
    pd("DB::starting db_connection (db-init)")
    conn2 = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass,db=db_db )
except:
    print "[-]ERROR DB::db-connection-error (db-init)"
    sys.exit(2)

c2 = conn2.cursor()


if action == "show":
    print """

Available Bots:
    
    """
    os.system("%s -l" % api)

    print """

Available RDF_providers:
    
    """
    prov = "select distinct(provider) from rdf_entries order by provider"
    c2.execute(prov)
    px = c2.fetchall()
    for x in px:
        print "  ->  %s " % x

    c2.close()
    sys.exit()
    
if bot == "":
    print helP
    sys.exit()


if providers[0] == "all":
    prov = "select distinct(provider) from rdf_entries order by provider"
    c2.execute(prov)
    providers = c2.fetchall()
    p_select = "'%s'" % providers[0][0]
    if len(providers) > 1:
        for p in providers[1:]:
            p_select = "%s or provider = '%s'" % (p_select, p[0])
else:
    p_select = "'%s'" % providers[0]
    if len(providers) > 1:
        for p in providers[1:]:
            p_select = "%s or provider = '%s'" % (p_select, p)


secshun = "select title, link, descu, id, provider from rdf_entries where diabot_seen != '1' and ( provider = %s )  order by id " % (p_select)
print secshun

c2.execute(secshun)
res = c2.fetchall()

for r in res:
    ts = time.time()
    idx = r[3]
    title = r[0].replace("\"", "'").strip()
    link = r[1].replace("\"", "'").strip()
    desc = r[2].replace("\"", "'")
    if desc == title:
        desc = "nono"
    rdf_provider = r[4]
    if rdf_provider == "xkcd":
        dx = desc.split("src=")[1]
        dx = dx.split(" ")[0].replace("\"", " ").strip()
        desc = """\n\n![XKCD](%s) \n\n""" % dx.replace("'", "")
        print "DESC: %s " % desc 
    msg = """## <a href="%s" target="_blank">%s</a>
---------------------------------
### Stream  : %s
### Link    : %s
---------------------------------

%s 

---------------------------------
%s :: %s 

#botpost #pistosapibot #%s """ % (link, title, rdf_provider, link, desc,  ts, idx, rdf_provider) 
    #print exe
    i = sub.call("""%s -d -u %s -t  "%s" """ % (api,bot, msg.replace("\"", "'")), shell=True)

    if i == 0:
        set_seen = "update rdf_entries set diabot_seen = '1' where id = '%s' " % idx
        c2.execute(set_seen)
        print "[+] OK updated [ %s ]\n\n\n" % idx
    else:
        print "[-] ERROR [ %s :: %s ]  \n\n\n" % (i, idx)
        time.sleep(2)
    # otherwise -> 503
    time.sleep(5)
    
    
    
c2.close()


print """


... exiting

"""
