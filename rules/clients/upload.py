#!/usr/bin/python
# Author: Anthony Ruhier
# QoS for upload

import tools
from config import PUBLIC_IF, UPLOAD


def interactive_class():
    """
    Interactive Class, for low latency, high priority packets such as VOIP and
    DNS.

    Low priority, pass before everything else. Uses htb then pfifo.
    """
    parent = "1:11"
    classid = "1:110"
    prio = 10
    mark = 110
    rate = UPLOAD * 10/100
    ceil = UPLOAD * 75/100
    minimum_ping = 10/1000
    expected_ping = 20/1000

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=expected_ping * rate,
                    cburst=minimum_ping * ceil, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="pfifo")
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def tcp_ack_class():
    """
    Class for TCP ACK.

    It's important to let the ACKs leave the network as fast
    as possible when a host of the network is downloading. Uses htb then sfq.
    """
    parent = "1:11"
    classid = "1:120"
    prio = 20
    mark = 120
    rate = UPLOAD/2
    ceil = UPLOAD
    expected_ping = 30/1000

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=expected_ping * rate, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def ssh_class():
    """
    Class for SSH connections.

    We want the ssh connections to be smooth !
    SFQ will mix the packets if there are several SSH connections in parallel
    and ensure that none has the priority
    """
    parent = "1:11"
    classid = "1:1100"
    prio = 30
    mark = 1100
    rate = UPLOAD * 10/100
    ceil = UPLOAD
    expected_ping = 25/1000
    minimum_ping = 10/1000

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=expected_ping * rate,
                    cburst=minimum_ping * ceil, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def http_class():
    """
    Class for HTTP/HTTPS connections.
    """
    parent = "1:11"
    classid = "1:1200"
    prio = 40
    mark = 1200
    rate = UPLOAD * 20/100
    ceil = UPLOAD
    expected_ping = 40/1000

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=expected_ping * rate, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def default_class():
    """
    Default class
    """
    parent = "1:11"
    classid = "1:1500"
    prio = 100
    mark = 1500
    rate = UPLOAD/2
    ceil = UPLOAD
    expected_ping = 40/1000

    tools.class_add(PUBLIC_IF, parent, classid, rate=rate, ceil=ceil,
                    burst=expected_ping * rate, prio=prio)
    tools.qdisc_add(PUBLIC_IF, parent=classid,
                    handle=tools.get_child_qdiscid(classid),
                    algorithm="sfq", perturb=10)
    tools.filter_add(PUBLIC_IF, parent="1:0", prio=prio, handle=mark,
                     flowid=classid)


def apply_qos():
    """
    Apply the QoS for the OUTPUT
    """
    # Creating the client branch (htb)
    tools.class_add(PUBLIC_IF, parent="1:1", classid="1:11",
                    rate=UPLOAD/2, ceil=UPLOAD,
                    burst=30 * UPLOAD/2, cburst=10 * UPLOAD,
                    prio=0)

    interactive_class()
    tcp_ack_class()
    ssh_class()
    http_class()
    default_class()
