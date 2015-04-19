#!/usr/bin/python

from config import INTERFACES
from built_in_classes import Root_tc_class
from .clients import Main as Clients
from .servers import Main as Servers


def apply_qos():
    GRE_ONLINE = INTERFACES["gre_online"]
    root_class = Root_tc_class(
            interface=GRE_ONLINE["name"],
            rate=GRE_ONLINE["speed"],
            burst=GRE_ONLINE["speed"]/8,
            qdisc_prefix_id="1:",
            default=1500
        )
    root_class.add_child(Clients())
    root_class.add_child(Servers())

    root_class.apply_qos()
