#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import UPLOAD
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFO_class, SFQ_class, Basic_tc_class

MAX_UPLOAD = UPLOAD * 0.98
MIN_UPLOAD = UPLOAD/10


class Interactive(PFIFO_class):
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    classid = "1:210"
    prio = 10
    mark = 210
    rate = MAX_UPLOAD * 10/100
    ceil = MAX_UPLOAD * 90/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class OpenVPN(SFQ_class):
    """
    Class for openvpn.

    We want openvpn to be fast. Uses htb then sfq.
    """
    classid = "1:215"
    prio = 15
    mark = 215
    rate = MAX_UPLOAD/3
    ceil = MAX_UPLOAD
    burst = burst_formula(rate) * 2
    cburst = cburst_formula(rate, burst)


class TCP_ack(SFQ_class):
    """
    Class for TCP ACK.

    It's important to let the ACKs leave the network as fast
    as possible when a host of the network is downloading. Uses htb then sfq.
    """
    classid = "1:220"
    prio = 20
    mark = 220
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class IRC(SFQ_class):
    """
    Class for IRC or services that doesn't need a lot of bandwidth but have to
    be quick.

    A bit low priority, htb then sfq.
    """
    classid = "1:2100"
    prio = 30
    mark = 2100
    rate = 100
    ceil = MAX_UPLOAD/5
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQ_class):
    """
    Default class

    Uses htb then sfq
    """
    classid = "1:2500"
    prio = 100
    mark = 2500
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Torrents(SFQ_class):
    """
    Class for torrents

    Very low priority. Uses htb then sfq
    """
    classid = "1:2600"
    prio = 150
    mark = 2600
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Main(Basic_tc_class):
    classid = "1:12"
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
    prio = 1

    def __init__(self, *args, **kwargs):
        r = super().__init__(*args, **kwargs)
        self.add_child(Interactive())
        self.add_child(OpenVPN())
        self.add_child(TCP_ack())
        self.add_child(IRC())
        self.add_child(Default())
        self.add_child(Torrents())
        return r
