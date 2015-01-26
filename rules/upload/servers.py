#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

import tools
from config import INTERFACES, UPLOAD
from rules.qos_formulas import burst_formula, cburst_formula

MIN_UPLOAD = UPLOAD/10
MAX_UPLOAD = UPLOAD
GRE_HOME = INTERFACES["gre_home"]


def interactive_class():
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    parent = "1:12"
    classid = "1:210"
    prio = 10
    mark = 210
    rate = MAX_UPLOAD * 10/100
    ceil = MAX_UPLOAD * 90/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="pfifo")
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def openvpn_class():
    """
    Class for openvpn.

    We want openvpn to be fast. Uses htb then sfq.
    """
    parent = "1:12"
    classid = "1:215"
    prio = 15
    mark = 215
    rate = UPLOAD  # It has to send almost the same data it receives
    ceil = UPLOAD * 2
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def tcp_ack_class():
    """
    Class for TCP ACK.

    It's important to let the ACKs leave the network as fast
    as possible when a host of the network is downloading. Uses htb then sfq.
    """
    parent = "1:12"
    classid = "1:220"
    prio = 20
    mark = 220
    rate = UPLOAD / 10
    ceil = MAX_UPLOAD / 10
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def irc_class():
    """
    Class for IRC or services that doesn't need a lot of bandwidth but have to
    be quick.

    A bit low priority, htb then sfq.
    """
    parent = "1:12"
    classid = "1:2100"
    prio = 30
    mark = 2100
    rate = 100
    ceil = MAX_UPLOAD/100
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def downloads_class():
    """
    Class for torrents and direct downloads

    A bit high priority, I don't want to wait for my movie :p. Uses htb then
    sfq
    """
    parent = "1:12"
    classid = "1:2600"
    prio = 50
    mark = 2600
    rate = MAX_UPLOAD * 20/100
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def default_class():
    """
    Default class

    Uses htb then sfq
    """
    parent = "1:12"
    classid = "1:2500"
    prio = 100
    mark = 2500
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(GRE_HOME, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(GRE_HOME, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(GRE_HOME, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def apply_qos():
    """
    Apply the QoS for the OUTPUT
    """
    # Creating the server branch (htb)
    # We want the client to be prioritary
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)
    tools.class_add(GRE_HOME, parent="1:1", classid="1:12", rate=rate,
                    ceil=ceil, burst=burst, cburst=cburst, prio=1)

    interactive_class()
    openvpn_class()
    tcp_ack_class()
    irc_class()
    downloads_class()
    default_class()
