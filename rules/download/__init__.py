#!/usr/bin/python

from config import INTERFACES, DOWNLOAD
from rules.qos_formulas import burst_formula
from built_in_classes import Root_tc_class
from .clients import Main as Clients
from .servers import Main as Servers


def apply_qos():
    LAN_IF = INTERFACES["lan_if"]
    root_class = Root_tc_class(
            interface=LAN_IF,
            rate=DOWNLOAD,
            ceil=DOWNLOAD,
            burst=burst_formula(DOWNLOAD)*3,
            qdisc_prefix_id="1:",
            default=1500
        )
    root_class.add_child(Clients())
    root_class.add_child(Servers())

    root_class.apply_qos()
