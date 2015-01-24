#!/usr/bin/python

import tools
from config import INTERFACES, DOWNLOAD
from rules import download


def apply_qos():
    openvpn_if = INTERFACES["openvpn"]
    # Creating the HTB root qdisc
    tools.qdisc_add(openvpn_if, "1:", "htb", default=1500)
    # Creating the main branch (htb)
    tools.class_add(openvpn_if, parent="1:0", classid="1:1", rate=DOWNLOAD,
                    ceil=DOWNLOAD, burst=DOWNLOAD/8)
    download.apply_qos()
