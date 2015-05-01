#!/usr/bin/python

from config import INTERFACES
from rules.qos_formulas import burst_formula
from built_in_classes import RootHTBClass
from .intervlan import InterVlan as InterVlan
from .external_trafic import Main as ExternalTrafic


def apply_qos():
    lan_if = INTERFACES["lan_if"]
    root_class = RootHTBClass(
        interface=lan_if["name"],
        rate=lan_if["if_speed"],
        ceil=lan_if["if_speed"],
        burst=burst_formula(lan_if["if_speed"]),
        qdisc_prefix_id="1:",
        default=10,
    )

    root_class.add_child(InterVlan())
    root_class.add_child(ExternalTrafic())

    root_class.apply_qos()
