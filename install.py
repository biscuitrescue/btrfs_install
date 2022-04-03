#!/usr/bin/env python3

from os.path import exists
from subprocess import run
from shutil import copyfile
from modules import install, install_all, install_more

### Install packages

while True:
    yes_no=input("Do you want to install all packages[Y/N]: ")
    if yes_no not in "YyNn":
        print("Invalid response. Please enter again")
    else:
        if yes_no in "nN":
            waste_of_time=False
            break
        elif yes_no in "yY":
            waste_of_time=True
            break

### Check for USB

while True:
    usb=input("Are you installing to an external disk?[Y/N]: ")
    if usb not in "YyNn":
        print("Invalid response. Please enter again")
    else:
        if usb in "nN":
            is_usb=False
            break
        elif usb in "yY":
            is_usb=True
            break

### Check for UEFI

if exists("/sys/firmware/efi"):
    UEFI=True
    if is_usb==True:
        grub_disk=input("Enter your grub device: ")

else:
    grub_disk=input("Enter your grub device: ")
    UEFI=False


### USERS and PASSES

copyfile("configs/pacman.conf", "/etc/pacman.conf")

user_name=input("Enter your username: ")
cmd="useradd -mG tty,video,audio,lp,input,audio,wheel {}".format(user_name)

run(cmd, shell=True)
print()

cmd="passwd "+user_name
run(cmd, shell=True)
print()

print("Enter password for root user: ")
run("passwd")
print()

### Locales

print("Configuring Locales ...")
print()


with open("/etc/locale.gen") as f:
    locale_gen=f.readlines()

for i in locale_gen:
    if i.strip()=="#en_US.UTF-8 UTF-8":
        i="en_US.UTF-8 UTF-8\n"

with open("/etc/locale.gen", "w") as f:
    for i in locale_gen:
        f.write(i)

run("locale-gen")

with open("/etc/locale.conf", "w") as f:
    f.write("LANG=en_US.UTF-8\n")

print("Locales are done")
print()

### Timezones

print("Configuring Timezones ...")
run("ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime", shell=True)
run(["hwclock", "--systohc"])
print("Timezones have been configured")

print()

### Configuring hostname & network

host_name=input("Enter hostname: ")

with open("/etc/hostname", "w") as f:
    f.write(host_name)

print()

print("Configuring Networking ...")

with open("/etc/hosts", "a") as f:
    f.write("127.0.0.1\t\tlocalhost")
    f.write("::1\t\tlocalhost")
    f.write("127.0.1.1\t\t{}".format(host_name))

print("Network has been configured")
print()

### Configuring sudo

print("Configuring sudo ...")
copyfile("configs/sudoers", "/etc/sudoers")
print("Done")
print()

### Installin packages

print("Installing some packages")
packages=[
    "f2fs-tools",
    "xfsprogs",
    "xfsdump",
    "pipewire",
    "pipewire-pulse",
    "pipewire-alsa",
    "pipewire-jack",
    "wireplumber",
    "pulseaudio-alsa",
    "grub",
    "alsa",
    "alsa-utils",
    "grub-btrfs",
    "dosfstools",
    "mtools",
    "btrfs-progs",
    "linux-headers",
    "ntp",
    "tlp",
    "networkmanager",
    "network-manager-applet",
    "xorg-server",
    "vim",
    "systemd-swap",
]

print()
install_more(packages)
print()

print("Installing Grub")

if is_usb:
    copyfile("configs/mkinitcpio.conf", "/etc/mkinicpio.conf")
    run(["mkinitcpio", "-P"])
    run("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --removable --recheck", shell=True)
    run(f"grub-install --target=i386-pc {grub_disk}", shell=True)
else:
    if UEFI:
        install("efibootmgr")
        run("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --removable --recheck", shell=True)
    else:
        run(f"grub-install --target=i386-pc {grub_disk}", shell=True)

run("grub-mkconfig -o /boot/grub/grub.cfg", shell=True)

print("Grub has been configured")
print()

p1 = run("df -h | grep -w / | awk '{print $1}'",shell=True,capture_output=True,text=True)
if 'nvme' in p1.stdout.strip():
    disk=p1.stdout.strip()[:-2]
else:
    disk=p1.stdout.strip()[:-1]

diskfile=f"/sys/block/{disk[5:]}/queue/rotational"

ssd=False
with open(diskfile) as f:
    if f.readlines()[0].strip()=='0':
        ssd=True

enable=[
    "NetworkManager",
    "systemd-swap",
    "ntpd",
]

if ssd:
    enable.append("fstrim.timer")

for service in enable:
    cmd=f"systemctl enable {service}"
    run(cmd, shell=True)

print()
print(f"Base system has been installed\nPlease run post-install.py as {user_name} after rebooting")
print()
print("Terminating ...")
