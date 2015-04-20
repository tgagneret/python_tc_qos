#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import INTERFACES
from built_in_classes import PFIFO_class
from rules.qos_formulas import burst_formula

LAN_IF_SPEED = INTERFACES["lan_if"]["if_speed"]


class InterVlan(PFIFO_class):
    """
    Intervlan need to be fast
    """
    classid = "1:15"
    rate = LAN_IF_SPEED
    ceil = LAN_IF_SPEED
    burst = burst_formula(rate) * 3
    prio = 0
    mark = 10
