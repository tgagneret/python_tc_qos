#!/usr/bin/python

from config import INTERFACES
from rules.qos_formulas import burst_formula
from built_in_classes import BasicHTBClass
from .clients import Main as Clients
from .servers import Main as Servers

DOWNLOAD = INTERFACES["lan_if"]["speed"]


class Main(BasicHTBClass):
    classid = "1:10"
    prio = 0
    rate = DOWNLOAD
    ceil = DOWNLOAD
    burst = burst_formula(rate) * 3
    qdisc_prefix_id = "1:"
    default = 10

    def __init__(self, *args, **kwargs):
        r = super().__init__(*args, **kwargs)
        self.add_child(Clients())
        self.add_child(Servers())
