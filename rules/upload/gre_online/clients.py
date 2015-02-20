#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import UPLOAD
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFO_class, SFQ_class, Basic_tc_class

MAX_UPLOAD = UPLOAD * 0.98


class Interactive(PFIFO_class):
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    classid = "1:110"
    prio = 10
    mark = 110
    rate = MAX_UPLOAD * 10/100
    ceil = MAX_UPLOAD * 90/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class TCP_ack(SFQ_class):
    """
    Class for TCP ACK.

    It's important to let the ACKs leave the network as fast
    as possible when a host of the network is downloading. Uses htb then sfq.
    """
    classid = "1:120"
    prio = 20
    mark = 120
    rate = MAX_UPLOAD / 4
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class SSH(SFQ_class):
    """
    Class for SSH connections.

    We want the ssh connections to be smooth !
    SFQ will mix the packets if there are several SSH connections in parallel
    and ensure that none has the priority
    """
    classid = "1:1100"
    prio = 30
    mark = 1100
    rate = MAX_UPLOAD * 10/100
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class HTTP(SFQ_class):
    """
    Class for HTTP/HTTPS connections.
    """
    classid = "1:1200"
    prio = 40
    mark = 1200
    rate = MAX_UPLOAD * 20/100
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQ_class):
    """
    Default class
    """
    classid = "1:1500"
    prio = 100
    mark = 1500
    rate = MAX_UPLOAD/2
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Main(Basic_tc_class):
    classid = "1:11"
    rate = UPLOAD/2
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
    prio = 0

    def __init__(self, *args, **kwargs):
        r = super().__init__(*args, **kwargs)
        self.add_child(Interactive())
        self.add_child(TCP_ack())
        self.add_child(SSH())
        self.add_child(HTTP())
        self.add_child(Default())
        return r
