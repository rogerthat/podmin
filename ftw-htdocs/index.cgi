#!/usr/bin/python
# -*- encoding: UTF-8 -*-
#
# small interface for ftw


version = "0.0.0.1"


import getpass, cgi, time, glob, string, hashlib, sys

podmin_root = "../"
podmin_lib = "%s/lib" % podmin_root
podmin_conf = "%s/conf" % podmin_root

sys.path.append(podmin_root)
sys.path.append(podmin_conf)
sys.path.append(podmin_lib)


from ftw_config import *
from ftw_func import *

# hom many tests backwards schall be displayed
test_sel_hours = "48"

# check if basic_auth

debug = "yes"

print "Content-Type: text/html \r\n\r\n"



bg_ok = "#BDFFBD"
bg_susp = "#FFED96"
bg_spam = "#FFB751"
bg_rep = "magenta"
bg_mal = "#FF7C8C"
bg_unk = "#C4E4E2"

header = """
<html>
<head>
<title>FederationTestWarrior - Results</title>
</head>
<body bgcolor='%s'>
<div align="center">
[ <a href="index.cgi">Index</a>   ]  ::
[ <a href="index.cgi?schedules=yes">Schedules</a>   ]
<hr>

"""


footer = """
</div>
</body>
</html>

"""


def main():
    global form
    form = cgi.FieldStorage()
    try:
        conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass,db=db_db )
        pd("DB::starting db_connection (db-init)")

    except:
        head = header % "black"
        print "%s " % (head)

        print """
<br><br>

<a href="https://c0unt.org/ftw"><img src="https://c0unt.org/ftw/guru_meditation.png" border="0"></a>

<br><br>
        """

        print footer
        sys.exit()

    head = header % "white"

    print head


    nt = int(time.time())
    sel_time = nt - (int(test_sel_hours)*(3600))
    dbx = "SELECT tests.testid, tests.ftwinit, tests.init_time from tests  where tests.init_time > '%s' order by init_time DESC;" % (sel_time)

    c = conn.cursor()
    c.execute(dbx)
    res = c.fetchall()



    try:
        int(res)
        print "[-] ERROR [%s] while trying to get results for interface" % res
        print footer
        sys.exit()
    except:
        # we got result, even if emtpy
        pass


    if form.has_key("q"):
        skey = form["q"].value
        for r in res:
            testid = r[0]
            testid_txt = "%s..." % testid[0:7]
            ftwinit = r[1]
            init_time = int(r[2])
            init_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(init_time)))
            if skey == testid:

                print """<h2><a href="index.cgi">displaying %s testid: %s</h2>""" % (ftwinit, skey)

                print """

                <table border="1" cellpadding="10" >
                <tr><td colspan="3">finished</td></tr>
                <tr><td>account</td><td>status</td><td>checked_time</td></tr>

                """

                dbx = "SELECT account, status, checked_time from test_results  where testid = '%s' and checked != '0' order by  status, checked_time;" % (skey)

                c = conn.cursor()
                c.execute(dbx)
                mres = c.fetchall()
                for mr in mres:
                    account = mr[0]
                    status = mr[1]
                    checked_time = mr[2]
                    if int(checked_time) == 0:
                        checked_date = "..."
                    else:
                        checked_date =  time.strftime("%Y-%m-%d %H:%M", time.localtime(float(checked_time)))
                    print """
                    <tr><td>%s</td><td>%s</td><td>%s</td></tr>
                    """ % (account, status, checked_date)

                dbx = "SELECT account, status, checked_time from test_results  where testid = '%s' and checked = '0' order by  id;" % (skey)


                c = conn.cursor()
                c.execute(dbx)
                mres = c.fetchall()

                print """
                <tr><td colspan="3">waiting</td></tr>

                """

                for mr in mres:
                    account = mr[0]
                    status = mr[1]
                    checked_time = mr[2]
                    if int(checked_time) == 0:
                        checked_date = "..."
                    else:
                        checked_date =  time.strftime("%Y-%m-%d %H:%M", time.localtime(float(checked_time)))
                    print """
                    <tr><td>%s</td><td>%s</td><td>%s</td></tr>
                    """ % (account, status, checked_date)


                dbx = "SELECT start_time from schedules  where testid = '%s' and status != '1' order by  start_time;" % (skey)


                c = conn.cursor()
                c.execute(dbx)
                mres = c.fetchall()
                print """
                <tr><td colspan="3">planned Schedules</td></tr>
                """
                for mr in mres:
                    start_time = mr[0]
                    start_date =  time.strftime("%Y-%m-%d %H:%M", time.localtime(float(start_time)))
                    print """
                    <tr><td colspan="3">%s</td></tr>
                    """ % start_date
                print """


                </table>
                """


                break


    elif form.has_key("schedules"):


        dbx = "SELECT start_time, testid from schedules where start_time > '%s' order by  start_time;" % (nt)


        c = conn.cursor()
        c.execute(dbx)
        mres = c.fetchall()
        print """
        <table border="1" cellpadding="10" >
        """
        for mr in mres:
            start_time = mr[0]
            testid = mr[1]
            testid_txt = "%s..." % testid[0:7]

            start_date =  time.strftime("%Y-%m-%d %H:%M", time.localtime(float(start_time)))
            print """
            <tr><td><a href="index.cgi?q=%s">%s</a></td><td>%s</td>
            """ % (testid, testid_txt, start_date)
        print "</table>"

    else:




        print """
    <table border="1"  cellpadding="10">
    <tr><td>TestID</td><td>FTWInit</td><td>StartDate</td></tr>

        """
        for r in res:
            testid = r[0]
            testid_txt = "%s..." % testid[0:5]
            ftwinit = r[1]
            init_time = int(r[2])
            init_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(init_time)))
            print """

            <tr><td><a href="index.cgi?q=%s" alt="%s">%s</a></td><td>%s</td><td>%s</td></tr>

            """ % (testid, testid_txt, testid_txt, ftwinit, init_date)

        print "</table>"

    conn.close()
    print footer


main()
sys.exit()
