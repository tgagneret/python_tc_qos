#!/usr/bin/python

from config import INTERFACES
from built_in_classes import RootHTBClass
from .servers import GRE_online, Default, Torrents


def apply_qos():
    public_if = INTERFACES["public_if"]
    root_class = RootHTBClass(
        interface=public_if["name"],
        rate=public_if["speed"],
        burst=public_if["speed"]/8,
        qdisc_prefix_id="1:",
        default=500
    )
    root_class.add_child(GRE_online())
    root_class.add_child(Default())
    root_class.add_child(Torrents())

    root_class.apply_qos()
