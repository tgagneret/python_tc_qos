#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

import tools
from config import INTERFACES, UPLOAD
from rules.qos_formulas import burst_formula, cburst_formula

MIN_UPLOAD = UPLOAD/10
MAX_UPLOAD = UPLOAD
PUBLIC_IF = INTERFACES["public_if"]


def gre_online():
    """
    Class for gre_tunnel

    As almost all traffic is going through the tunnel, very high priority.
    Uses htb then sfq
    """
    parent = "1:1"
    classid = "1:100"
    prio = 20
    mark = 100
    rate = UPLOAD * 0.8
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def default_class():
    """
    Class for gre_tunnel

    As almost all traffic is going through the tunnel, very high priority.
    Uses htb then sfq
    """
    parent = "1:1"
    classid = "1:500"
    prio = 50
    mark = 500
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = burst_formula(rate)
    cburst = cburst_formula(rate, burst)

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def torrents_class():
    """
    Class for torrents

    Very low priority. Uses htb then sfq
    """
    parent = "1:1"
    classid = "1:600"
    prio = 100
    mark = 600
    rate = MIN_UPLOAD
    ceil = MAX_UPLOAD
    burst = 0.5 * rate/8
    cburst = cburst_formula(rate, burst)

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=burst, cburst=cburst, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def apply_qos():
    """
    Apply the QoS for the OUTPUT
    """
    gre_online()
    torrents_class()
    default_class()
