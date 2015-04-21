#!/usr/bin/python

from config import INTERFACES
from rules.qos_formulas import burst_formula
from built_in_classes import Root_tc_class
from .clients import Main as Clients
from .servers import Main as Servers


def apply_qos():
    GRE_HOME = INTERFACES["gre-home"]
    root_class = Root_tc_class(
        interface=GRE_HOME["name"],
        rate=GRE_HOME["speed"],
        burst=burst_formula(GRE_HOME["speed"]),
        qdisc_prefix_id="1:",
        default=1500
    )
    root_class.add_child(Clients())
    root_class.add_child(Servers())

    root_class.apply_qos()
