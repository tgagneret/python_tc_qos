#!/usr/bin/python

from config import INTERFACES, DOWNLOAD
from built_in_classes import Root_tc_class
from .download import Interactive, TCP_ack, SSH, HTTP, Default


def apply_qos():
    OPENVPN_IF = INTERFACES["openvpn"]
    root_class = Root_tc_class(
            interface=OPENVPN_IF,
            rate=DOWNLOAD * 30/100,
            ceil=DOWNLOAD,
            burst=DOWNLOAD/8,
            qdisc_prefix_id="1:",
            default=1500
        )
    root_class.add_child(Interactive())
    root_class.add_child(TCP_ack())
    root_class.add_child(SSH())
    root_class.add_child(HTTP())
    root_class.add_child(Default())

    root_class.apply_qos()
