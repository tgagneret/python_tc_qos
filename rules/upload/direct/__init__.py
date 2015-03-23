#!/usr/bin/python

from config import INTERFACES, UPLOAD
from built_in_classes import Root_tc_class
from .servers import GRE_online, Default, Torrents


def apply_qos():
    PUBLIC_IF = INTERFACES["public_if"]
    root_class = Root_tc_class(
            interface=PUBLIC_IF,
            rate=UPLOAD,
            burst=UPLOAD/8,
            qdisc_prefix_id="1:",
            default=500
        )
    root_class.add_child(GRE_online())
    root_class.add_child(Default())
    root_class.add_child(Torrents())

    root_class.apply_qos()
