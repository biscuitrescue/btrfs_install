#!/usr/bin/env python3

from os.path import exists
from subprocess import run
from shutil import copyfile
from modules import install, install_more, check_ssd

### Check for USB

while True:
    usb=input("Are you installing to an external disk?[Y/N]: ")
    if usb in "Yy":
        is_usb=True
        break
    elif usb in "Nn":
        is_usb=False
        break
    else:
        print("Invalid response. Please enter either y or n.")
        continue

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
cmd=f"useradd -mG tty,video,audio,lp,input,audio,wheel,network {user_name}"

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
    f.write(f"127.0.1.1\t\t{host_name}@localdomain\t\t{host_name}")

print("Network has been configured")
print()

### Configuring sudo

print("Configuring sudo ...")
copyfile("configs/sudoers", "/etc/sudoers")
print("Done")
print()

### Installing packages

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

enable=[
    "NetworkManager",
    "systemd-swap",
    "ntpd",
]

if check_ssd(diskfile):
    enable.append("fstrim.timer")

for service in enable:
    cmd=f"systemctl enable {service}"
    run(cmd, shell=True)

print()
print(f"Base system has been installed\nPlease run post-install.py as {user_name} after rebooting")
print()
print("Terminating ...")
