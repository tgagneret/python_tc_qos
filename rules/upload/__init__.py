#!/usr/bin/python

import tools
from config import INTERFACES, UPLOAD
from rules.qos_formulas import burst_formula
from rules.upload import clients, servers


def apply_qos():
    GRE_HOME = INTERFACES["gre_home"]
    tools.qdisc_add(GRE_HOME, "1:", "htb", default=1500)
    tools.class_add(GRE_HOME, parent="1:0", classid="1:1", rate=UPLOAD,
                    ceil=UPLOAD, burst=burst_formula(UPLOAD))
    clients.apply_qos()
    servers.apply_qos()
