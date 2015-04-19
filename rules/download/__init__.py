#!/usr/bin/python

from config import INTERFACES
from rules.qos_formulas import burst_formula
from built_in_classes import Root_tc_class
from .intervlan import InterVlan as InterVlan
from .external_trafic import Main as ExternalTrafic


def apply_qos():
    LAN_IF = INTERFACES["lan_if"]
    root_class = Root_tc_class(
            interface=LAN_IF["name"],
            rate=LAN_IF["if_speed"],
            ceil=LAN_IF["if_speed"],
            burst=burst_formula(LAN_IF["if_speed"])*3,
            qdisc_prefix_id="1:",
            default=10
        )

    root_class.add_child(InterVlan())
    root_class.add_child(ExternalTrafic())

    root_class.apply_qos()
