#!/usr/bin/python

import tools
from config import INTERFACES, DOWNLOAD
from rules.qos_formulas import burst_formula
from rules.download import clients, servers


def apply_qos():
    LAN_IF = INTERFACES["lan_if"]
    tools.qdisc_add(LAN_IF, "1:", "htb", default=1500)
    tools.class_add(LAN_IF, parent="1:0", classid="1:1", rate=DOWNLOAD,
                    ceil=DOWNLOAD, burst=burst_formula(DOWNLOAD)*3)
    clients.apply_qos()
    servers.apply_qos()
