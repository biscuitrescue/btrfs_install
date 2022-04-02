#!/usr/bin/env python3

from subprocess import run

def install(pkg):
    cmd="pacman --needed --noconfirm -S "+pkg
    run(cmd, shell=True)

def install_all(files):
    run("pacman --needed --noconfirm --ask 4 -S - < {}".format(files), shell=True)

def install_more(pkgs):
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
    cmd="paru -S {}".format(pkg)
    run(cmd, shell=True)
