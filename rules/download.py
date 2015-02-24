#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

from config import DOWNLOAD, UPLOAD
from rules.qos_formulas import burst_formula, cburst_formula
from built_in_classes import PFIFO_class, SFQ_class

MAX_DOWNLOAD = DOWNLOAD


class Interactive(PFIFO_class):
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    classid = "1:110"
    prio = 10
    mark = 110
    rate = MAX_DOWNLOAD * 10/100
    ceil = MAX_DOWNLOAD * 90/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class TCP_ack(SFQ_class):
    """
    Class for TCP ACK.

    It's important to receive quickly the TCP ACK when uploading. Uses htb then
    sfq.
    """
    classid = "1:120"
    prio = 20
    mark = 120
    rate = UPLOAD / 10
    ceil = MAX_DOWNLOAD / 10
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
    rate = 400
    ceil = MAX_DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class HTTP(SFQ_class):
    """
    Class for HTTP/HTTPS connections.
    """
    classid = "1:1200"
    prio = 40
    mark = 1200
    rate = MAX_DOWNLOAD * 10/100
    ceil = MAX_DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)


class Default(SFQ_class):
    """
    Default class
    """
    classid = "1:1500"
    prio = 100
    mark = 1500
    rate = MAX_DOWNLOAD * 20/100
    ceil = MAX_DOWNLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
