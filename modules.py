#!/usr/bin/env python3

def install(pkg: str):
    cmd=f"pacman --needed --noconfirm -S {pkg}"
    run(cmd, shell=True)

def install_more(pkgs: list):
    for i in range(0,len(pkgs),5):
        s=packages[i:i+5]
        for i in s:
            s2+=i.strip()+' '
        install(s2)

def install_all(files):
    s2=''
    with open(files) as f:
        x=f.readlines()
    install_more(x)

def paru(pkg: str):
    cmd=f"paru -S --needed --noconfirm {pkg}"
    run(cmd, shell=True)

def paru_more(pkgs: list):
    for i in range(0,len(pkgs),5):
        s=packages[i:i+5]
        for i in s:
            s2+=i.strip()+' '
        paru(s2)

def paru_all(files):
    s2=''
    with open(files) as f:
        x=f.readlines()
    paru_more(x)

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
