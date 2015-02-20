#!/usr/bin/python

from . import direct, gre_online


def apply_qos():
    direct.apply_qos()
    gre_online.apply_qos()
