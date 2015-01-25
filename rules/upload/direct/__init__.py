#!/usr/bin/python

import tools
from config import INTERFACES, UPLOAD
from rules.upload.direct import servers


def apply_qos():
    PUBLIC_IF = INTERFACES["public_if"]
    tools.qdisc_add(PUBLIC_IF, "1:", "htb", default=500)
    tools.class_add(PUBLIC_IF, parent="1:0", classid="1:1", rate=UPLOAD,
                    ceil=UPLOAD, burst=UPLOAD/8)
    servers.apply_qos()
