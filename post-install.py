#!/usr/bin/env python3

from os.path import exists
from os import mkdir, listdir
from shutil import copyfile
from subprocess import run

def copy_to_config():
    for i in condict:
        file_orig=f"configs/{i}"
        file_copy=f"{condict[i]}/{i}"
        copyfile(file_orig, file_copy)
    username=listdir("/home/")[0]
    cmd=f"chown -R {username}:{username} /home/{username}/.config/"
    run(cmd, shell=True)


with open('config.txt') as f:
    L = f.readlines()

for i in range(len(L)):
    L[i]=L[i].strip()
    L[i]=L[i].split()

condict={}
for i in L:
    condict[i[0]]=i[1]

for i in condict:
    if not exists(condict[i]):
        mkdir(condict[i])

copy_to_config()
