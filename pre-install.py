#!/usr/bin/env python3

from subprocess import run
from os.path import exists

def disk_check(s):
    p1 = run("lsblk | grep "+s+" -w | awk '{print $1}'",shell=True,capture_output=True,text=True)
    if p1.stdout.strip() !='':
        return True
    else:
        return False

while True: 
    disk=input('Disk name [/dev/sdX]: ')
    if disk_check(disk[5:]):
        print('Disk exists.')
        print()
        break
    else:
        print('Disk does not exist.')
        print()
        continue

resp=input('''
This program will completely wipe the disk.
Are you sure you want to proceed?
Type 'yes' in all capital letters to proceed: ''')

if resp!='YES':
    print('Cancelling...')
    exit()

print('Creating new partition table...')
run('parted '+disk+' mklabel gpt',shell=True)
print('Created new GPT partition table.')
print()

