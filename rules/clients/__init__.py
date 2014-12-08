#!/usr/bin/python

from rules.clients import download, upload


def apply_qos():
    download.apply_qos()
    upload.apply_qos()
