#!/usr/bin/python

import tools
from config import PUBLIC_IF, LAN_IF, UPLOAD
from rules import clients, servers


def apply_qos():
    # Creating the HTB root qdisc
    tools.qdisc_add(PUBLIC_IF, "1:", "htb")
    # Creating the main branch (htb)
    tools.class_add(PUBLIC_IF, parent="1:0", classid="1:1", rate=UPLOAD,
                    ceil=UPLOAD)
    tools.qdisc_add(LAN_IF, "1:", "htb", default=1900)
    clients.apply_qos()
    servers.apply_qos()
