#!/usr/bin/python
# Author: Anthony Ruhier

import tools


class Basic_tc_class():
    """
    Basic class
    """
    #: parent class
    _parent = None
    #: root class: class directly attached to the interface
    _root = None
    #: interface
    _interface = None
    #: class id
    classid = None
    #: rate
    rate = None
    #: ceil
    ceil = None
    #: burst
    burst = None
    #: cburst
    cburst = None
    #: priority
    prio = None
    #: children class which will be attached to this class
    children = None

    def __init__(self, classid=None, rate=None, ceil=None,
                 burst=None, cburst=None, prio=None, children=None, *args,
                 **kwargs):
        self.classid = classid if classid is not None else self.classid
        self.rate = rate if rate is not None else self.rate
        self.ceil = ceil if ceil is not None else self.ceil
        self.burst = burst if burst is not None else self.burst
        self.cburst = cburst if cburst is not None else self.cburst
        self.prio = prio if prio is not None else self.prio
        self.children = children if children is not None else []

    def add_child(self, class_child):
        """
        Add a class as children
        """
        class_child.set_parent_root(parent=self.classid)
        class_child.recursive_parent_change(self._root, self._interface)
        self.children.append(class_child)

    def recursive_parent_change(self, root=None, interface=None):
        """
        When rattaching a class to another class, have to change recursively
        the interface and root id of all children

        :param root: root id
        :param interface: interface of the parent
        """
        if root is not None:
            self._root = root
        if interface is not None:
            self._interface = interface
        for child in self.children:
            child.recursive_parent_change(root, interface)

    def _add_class(self):
        """
        Add class to the interface
        """
        tools.class_add(self._interface, parent=self._parent,
                        classid=self.classid, rate=self.rate,
                        ceil=self.ceil, burst=self.burst, cburst=self.cburst,
                        prio=self.prio)

    def apply_qos(self):
        """
        Apply qos with current attributes

        The function is recursive, so it will apply the qos of all children
        too.
        """
        self._add_class()
        for child in self.children:
            child.apply_qos()

    def set_parent_root(self, parent=None, root=None):
        """
        Set root and/or parent

        param parent: parent class id
        param root: root class id
        """
        if parent:
            self._parent = parent
        if root:
            self._root = root

    def set_interface(self, interface):
        """
        Set interface

        :param interface: interface to attach the class
        """
        self._interface = interface


class Root_tc_class(Basic_tc_class):
    """
    Root tc class, directly attached to the interface
    """
    #: main algorithm to use for the qdisc
    algorithm = None
    #: qdisc prefix
    qdisc_prefix_id = None
    #: default mark to catch
    default = None

    def __init__(self, interface=None, algorithm="htb", qdisc_prefix_id="1:",
                 default=None, *args, **kwargs):
        self._interface = interface
        self.algorithm = algorithm
        self.qdisc_prefix_id = qdisc_prefix_id
        self.default = default
        self._parent = str(self.qdisc_prefix_id) + "0"
        self._root = self._parent
        self.classid = str(self.qdisc_prefix_id) + "1"
        return super().__init__(*args, **kwargs)

    def _add_qdisc(self):
        """
        Add the root qdisc
        """
        tools.qdisc_add(self._interface, self.qdisc_prefix_id, self.algorithm,
                        default=self.default)

    def apply_qos(self):
        self._add_qdisc()
        return super().apply_qos()


class _Basic_filter_class(Basic_tc_class):
    """
    Basic class with filtering
    """
    #: mark catch by the class
    mark = None

    def __init__(self, mark=None, *args, **kwargs):
        self.mark = mark if mark is not None else self.mark
        super().__init__(*args, **kwargs)

    def _add_filter(self):
        """
        Add filter to the class
        """
        tools.filter_add(self._interface, parent=self._root, prio=self.prio,
                         handle=self.mark, flowid=self.classid)

    def _add_qdisc(self):
        raise NotImplemented

    def apply_qos(self):
        """
        Apply qos with current attributes

        The function is recursive, so it will apply the qos of all children
        too.
        """
        self._add_class()
        self._add_qdisc()
        self._add_filter()
        for child in self.children:
            child.apply_qos()


class SFQ_class(_Basic_filter_class):
    """
    Basic class with a SFQ qdisc builtin
    """
    #: perturb parameter for sfq
    perturb = None

    def __init__(self, perturb=10, *args, **kwargs):
        self.perturb = perturb
        super().__init__(*args, **kwargs)

    def _add_qdisc(self):
        tools.qdisc_add(self._interface, parent=self.classid,
                        handle=tools.get_child_qdiscid(self.classid),
                        algorithm="sfq", perturb=self.perturb)


class PFIFO_class(_Basic_filter_class):
    """
    Basic filtering class with a PFIFO qdisc built in
    """
    def _add_qdisc(self):
        tools.qdisc_add(self._interface, parent=self.classid,
                        handle=tools.get_child_qdiscid(self.classid),
                        algorithm="pfifo")
