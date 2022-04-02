#!/usr/bin/env python3

from subprocess import run
from os.path import exists

disk=input('Disk name: ')

resp=input('''
This program will completely wipe the disk.
Are you sure you want to proceed?
Type 'yes' in all capital letters to proceed: ''')

if resp!='YES':
    print('Cancelling...')
    exit()

