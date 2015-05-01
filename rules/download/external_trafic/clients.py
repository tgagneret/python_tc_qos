#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import INTERFACES
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFOClass, SFQClass, BasicHTBClass

DOWNLOAD = INTERFACES["lan_if"]["speed"]
UPLOAD = INTERFACES["public_if"]["speed"]


class Interactive(PFIFOClass):
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    classid = "1:110"
    prio = 10
    mark = 110
    rate = DOWNLOAD * 30/100
    ceil = DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class TCP_ack(SFQClass):
    """
    Class for TCP ACK.

    It's important to receive quickly the TCP ACK when uploading. Uses htb then
    sfq.
    """
    classid = "1:120"
    prio = 20
    mark = 120
    rate = UPLOAD / 10
    ceil = DOWNLOAD / 10
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class SSH(SFQClass):
    """
    Class for SSH connections.

    We want the ssh connections to be smooth !
    SFQ will mix the packets if there are several SSH connections in parallel
    and ensure that none has the priority
    """
    classid = "1:1100"
    prio = 30
    mark = 1100
    rate = 400
    ceil = DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class HTTP(SFQClass):
    """
    Class for HTTP/HTTPS connections.
    """
    classid = "1:1200"
    prio = 40
    mark = 1200
    rate = DOWNLOAD * 10/100
    ceil = DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQClass):
    """
    Default class
    """
    classid = "1:1500"
    prio = 100
    mark = 1500
    rate = DOWNLOAD * 20/100
    ceil = DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Main(BasicHTBClass):
    classid = "1:11"
    rate = DOWNLOAD * 70/100
    ceil = DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
    prio = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_child(Interactive())
        self.add_child(TCP_ack())
        self.add_child(SSH())
        self.add_child(HTTP())
        self.add_child(Default())
