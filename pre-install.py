#!/usr/bin/env python3

from subprocess import run
from os.path import exists
from modules import disk_check, check_ssd

while True:
    disk=input('Disk name [/dev/sdX or /dev/nvme0nX]: ')
    if disk_check(disk[5:]):
        print('Disk exists.')
        print()
        break
    else:
        print('Disk does not exist.')
        print()
        continue

diskfile=f"/sys/block/{disk[5:]}/queue/rotational"

resp=input('''
This program will completely wipe the disk.
Are you sure you want to proceed?
Type 'yes' in all capital letters to proceed: ''')

if resp!='YES':
    print('Cancelling...')
    exit()

### Partition Table ###
print('Creating new partition table...')
run(f'sfdisk --label {disk} gpt',shell=True)
print('Created new GPT partition table.')
print()

### Partitioning ###

print('Creating partitions...')
run()

### Filesystems ###
if disk.startswith('/dev/nvme'):
    part2=disk+'p2'
    part3=disk+'p3'
else:
    part2=disk+'2'
    part3=disk+'3'

run(f'mkfs.vfat -F32 {part2}',shell=True)
run(f'mkfs.btrfs {part3}',shell=True)


### Btrfs subvolumes ###
run(f'mount {part3} /mnt')
run('btrfs subvolume create /mnt/@',shell=True)
run('btrfs subvolume create /mnt/@var',shell=True)
run('btrfs subvolume create /mnt/@home',shell=True)
run('btrfs subvolume create /mnt/@tmp',shell=True)
run('umount /mnt',shell=True)

### Mounting subvolumes ###

p=""
if check_ssd(diskfile):
    p="ssd,"
# p="ssd," if ssd else ""
s=f'mount -o noatime,compress=zstd,discard=async,{p}subvol='

run(f'{s}@ {part3} /mnt',shell=True)
dirs=['home','boot','var','tmp']

for i in dirs:
    os.mkdir('/mnt/'+i)
    run(f'{s}@{i} {part3} /mnt/{i}', shell=True)

run(f'mount {part2} /mnt/boot',shell=True )
run('lsblk')
print()

### Pacstrap and genfstab ###
print('Running pacstrap...')
run('pacstrap /mnt base linux linux-firmware base-devel git python3 ranger btop htop vim wget arch-install-scripts --noconfirm --needed',shell=True)
run('genfstab -U /mnt >> /mnt/etc/fstab',shell=True)
print()
print('Pacstrap complete')
print()

print('Install script can be executed.')
