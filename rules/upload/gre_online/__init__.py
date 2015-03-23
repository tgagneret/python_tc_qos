#!/usr/bin/python

from config import INTERFACES, UPLOAD
from built_in_classes import Root_tc_class
from .clients import Main as Clients
from .servers import Main as Servers

MAX_UPLOAD = UPLOAD * 0.93


def apply_qos():
    GRE_ONLINE = INTERFACES["gre_online"]
    root_class = Root_tc_class(
            interface=GRE_ONLINE,
            rate=MAX_UPLOAD,
            burst=UPLOAD/8,
            qdisc_prefix_id="1:",
            default=1500
        )
    root_class.add_child(Clients())
    root_class.add_child(Servers())

    root_class.apply_qos()
