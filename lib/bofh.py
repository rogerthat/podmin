#!/usr/bin/python
#
# bofh.exe -> excuse-generatort for sysadmins
#
# 


version = "1.0.1 build.666 - stable - 2012-01-24"


from sys import path as syspath
from random import randrange
from os import path as ospath
from os import getenv
from sys import argv as sysargv
from sys import exit as sexit


def bofh_excuse():
    default_excuse = "Feature was not beta tested"
    

    
    excuses = "lib/bofh.excuses"
    
    if not ospath.isfile(excuses):
        print " [-] error ... excuse-file not found [ %s ] " 
        sexit(2)
    
    ifile = open(excuses).readlines()
    
    ilen = len(ifile)
    rline = ""
    if ilen < 5:
        rline = default_excuse
    
    while len(rline) < 5:
        gline = randrange(0,(ilen-1))
        rline = ifile[gline]

    return("%s" % rline.strip())
    
    
    sexit(0)

    
if __name__ == "__main__":

    if len(sysargv) > 1:
    
        print """
    
    ****************************************************************
    *
    * BOFH-ExEcuses for finer LART-Administration
    *      v: %s
    *
    ****************************************************************""" % version


    excuse = bofh_excuse()
    print "\n\n\n  BOFH  >  %s \n\n\n" % excuse
    
    sexit()
        
