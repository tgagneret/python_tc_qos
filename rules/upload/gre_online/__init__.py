#!/usr/bin/python

from config import INTERFACES
from built_in_classes import RootHTBClass
from .clients import Main as Clients
from .servers import Main as Servers


def apply_qos():
    gre_online = INTERFACES["gre_online"]
    root_class = RootHTBClass(
        interface=gre_online["name"],
        rate=gre_online["speed"],
        burst=gre_online["speed"]/8,
        qdisc_prefix_id="1:",
        default=1500
    )
    root_class.add_child(Clients())
    root_class.add_child(Servers())

    root_class.apply_qos()
