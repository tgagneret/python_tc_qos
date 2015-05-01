#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import INTERFACES
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFOClass, SFQClass, BasicHTBClass

GRE_UPLOAD = INTERFACES["gre_online"]["speed"]
MIN_UPLOAD = GRE_UPLOAD/10


class Interactive(PFIFOClass):
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    classid = "1:210"
    prio = 10
    mark = 210
    rate = GRE_UPLOAD * 10/100
    ceil = GRE_UPLOAD * 90/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class OpenVPN(SFQClass):
    """
    Class for openvpn.

    We want openvpn to be fast. Uses htb then sfq.
    """
    classid = "1:215"
    prio = 15
    mark = 215
    rate = GRE_UPLOAD/3
    ceil = GRE_UPLOAD
    burst = burst_formula(rate) * 2
    cburst = cburst_formula(rate, burst)


class TCP_ack(SFQClass):
    """
    Class for TCP ACK.

    It's important to let the ACKs leave the network as fast
    as possible when a host of the network is downloading. Uses htb then sfq.
    """
    classid = "1:220"
    prio = 20
    mark = 220
    rate = MIN_UPLOAD
    ceil = GRE_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class IRC(SFQClass):
    """
    Class for IRC or services that doesn't need a lot of bandwidth but have to
    be quick.

    A bit low priority, htb then sfq.
    """
    classid = "1:2100"
    prio = 30
    mark = 2100
    rate = 100
    ceil = GRE_UPLOAD/5
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQClass):
    """
    Default class

    Uses htb then sfq
    """
    classid = "1:2500"
    prio = 100
    mark = 2500
    rate = MIN_UPLOAD
    ceil = GRE_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Torrents(SFQClass):
    """
    Class for torrents

    Very low priority. Uses htb then sfq
    """
    classid = "1:2600"
    prio = 150
    mark = 2600
    rate = MIN_UPLOAD
    ceil = GRE_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Main(BasicHTBClass):
    classid = "1:12"
    rate = MIN_UPLOAD
    ceil = GRE_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
    prio = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_child(Interactive())
        self.add_child(OpenVPN())
        self.add_child(TCP_ack())
        self.add_child(IRC())
        self.add_child(Default())
        self.add_child(Torrents())
