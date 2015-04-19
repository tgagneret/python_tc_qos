#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import INTERFACES
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFO_class, SFQ_class

UPLOAD = INTERFACES["public_if"]["speed"]
MIN_UPLOAD = 200


class GRE_online(PFIFO_class):
    """
    Class for gre_tunnel

    As almost all traffic is going through the tunnel, very high priority.
    Uses htb then sfq
    """
    parent = "1:1"
    classid = "1:100"
    prio = 20
    mark = 100
    rate = UPLOAD - MIN_UPLOAD
    ceil = UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQ_class):
    """
    Class for gre_tunnel

    As almost all traffic is going through the tunnel, very high priority.
    Uses htb then sfq
    """
    classid = "1:500"
    prio = 50
    mark = 500
    rate = UPLOAD
    ceil = UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Torrents(SFQ_class):
    """
    Class for torrents

    Very low priority. Uses htb then sfq
    """
    classid = "1:600"
    prio = 100
    mark = 600
    rate = MIN_UPLOAD
    ceil = UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
