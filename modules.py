#!/usr/bin/env python3

from subprocess import run

def install(pkg: str):
    cmd=f"pacman --needed --noconfirm -S {pkg}"
    run(cmd, shell=True)

def install_all(files):
    #run(f"pacman --needed --noconfirm --ask 4 -S - < {files}", shell=True)
    
    for i in range(0,len(),5):
        s=packages[i:i+5]
        install_more(s)

def install_more(pkgs: list):
    with open("packages.txt", "w") as f:
        for i in pkgs:
            f.write(i+'\n')
    install_all("packages.txt")

def paru(pkg):
    cmd=f"paru -S --needed --noconfirm {pkg}"
    run(cmd, shell=True)

def disk_check(s):
    p1 = run("lsblk | grep "+s+" -w | awk '{print $1}'",shell=True,capture_output=True,text=True)
    if p1.stdout.strip() !='':
        return True
    else:
        return False

def check_ssd(disk):

    p1 = run("df -h | grep -w / | awk '{print $1}'",shell=True,capture_output=True,text=True)
    if 'nvme' in p1.stdout.strip():
        disk=p1.stdout.strip()[:-2]
    else:
        disk=p1.stdout.strip()[:-1]

    diskfile=f"/sys/block/{disk[5:]}/queue/rotational"

    with open(diskfile) as f:
        ssd=True if f.readlines()[0].strip()=='0' else False
        return ssd
