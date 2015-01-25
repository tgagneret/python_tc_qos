#!/usr/bin/python

from rules import download, upload


def apply_qos():
    download.apply_qos()
    upload.apply_qos()
