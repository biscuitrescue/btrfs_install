#!/usr/bin/env python3

from os.path import exists
from os import mkdir
from shutil import copyfile

for i in condict:
    if not exists(condict[i]):
        mkdir(condict[i])

for i in condict:
    file_orig=f"configs/{i}"
    file_copy=f"{condict[i]}/{i}"
    copyfile(file_orig, file_copy)
