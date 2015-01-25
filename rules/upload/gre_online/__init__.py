#!/usr/bin/python

import tools
from config import INTERFACES, UPLOAD
from rules.upload.gre_online import clients, servers


def apply_qos():
    GRE_ONLINE = INTERFACES["gre_online"]
    # Creating the HTB root qdisc
    tools.qdisc_add(GRE_ONLINE, "1:", "htb", default=1500)
    # Creating the main branch (htb)
    tools.class_add(GRE_ONLINE, parent="1:0", classid="1:1", rate=UPLOAD,
                    ceil=UPLOAD, burst=UPLOAD/8)
    clients.apply_qos()
    servers.apply_qos()
