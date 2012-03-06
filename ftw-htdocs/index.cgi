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

# check if basic_auth

debug = "yes"

print "Content-Type: text/html \r\n\r\n"


bg_ok = "#BDFFBD"
bg_susp = "#FFED96"
bg_spam = "#FFB751"
bg_rep = "magenta"
bg_mal = "#FF7C8C"
bg_unk = "#C4E4E2"


def main():
    pass




main()
