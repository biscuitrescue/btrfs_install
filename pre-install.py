#!/usr/bin/env python3

from subprocess import run
from os.path import exists

if exists("/sys/firmware/efi"):
    UEFI=True
else:
    UEFI=False
