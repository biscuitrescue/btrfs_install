#!/usr/bin/env python3

from subprocess import run

def install(pkg):
    cmd=f"pacman --needed --noconfirm -S {pkg}"
    run(cmd, shell=True)

def install_all(files):
    run(f"pacman --needed --noconfirm --ask 4 -S - < {files}", shell=True)

def install_more(pkgs: list):
    with open("packages.txt", "w") as f:
        for i in pkgs:
            f.write(i+'\n')
    install_all("packages.txt")

def check_installed(pkg):
    paru=run(
        "pacman -Qqe",
        shell=True,
        capture_output=True,
        text=True,
    )

    pkgs=paru.stdout.split()

    if pkg in pkgs:
        installed=True
    else:
        installed=False

    return installed

def paru(pkg):
    cmd=f"paru -S --needed {pkg}"
    run(cmd, shell=True)

def disk_check(s):
    p1 = run("lsblk | grep "+s+" -w | awk '{print $1}'",shell=True,capture_output=True,text=True)
    if p1.stdout.strip() !='':
        return True
    else:
        return False

def check_ssd(disk):
    with open(diskfile) as f:
        ssd=True if f.readlines()[0].strip()=='0' else False
