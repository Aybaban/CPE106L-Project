# Community Ride Scheduling Application: Setup & Run Guide

This document provides a complete, step-by-step guide to set up and run the "Community Ride Scheduling Application" project. The project consists of a FastAPI backend (using MongoDB), a Flet desktop frontend, and Matplotlib visualization utilities.

## 1. Project Overview

- **Purpose:** To help elderly or individuals with accessibility needs schedule rides with local volunteers or services.

- **Backend (FastAPI):** Handles ride matching, scheduling, user/volunteer management, and interacts with the database. Uses MongoDB for data storage.

- **Frontend (Flet):** A desktop application for booking rides and managing schedules.

- **Visualization (Matplotlib):** Utility scripts to visualize ride data (e.g., frequency, wait times).


## 2. Prerequisites
Before you begin, ensure you have the following installed on your host machine (the computer running VirtualBox) and your Ubuntu 22.04 Virtual Machine.

### 2.1. On Your Host Machine
VirtualBox: Download and install the latest version from [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

### 2.2. On Your Ubuntu 22.04 Virtual Machine
- Ubuntu 22.04 LTS Desktop: Installed as a guest operating system in VirtualBox.

- VirtualBox Guest Additions: Installed within the Ubuntu VM for better performance and integration (e.g., screen resizing, shared clipboard).

- Python 3.10+: Ubuntu 22.04 comes with Python 3.10 pre-installed.

- ```pip``` and ```venv```: Python package installer and virtual environment tool.

- MongoDB Community Edition: The database server.

## 3. VirtualBox & Ubuntu 22.04 Setup (Detailed Steps)
Follow these steps to prepare your development environment.

### 3.1. Install VirtualBox (on Host Machine)
Download VirtualBox from the official website.

Run the installer and follow the on-screen prompts.

### 3.2. Download Ubuntu 22.04 LTS (on Host Machine)
Download the Ubuntu Desktop 22.04 LTS ISO image from https://ubuntu.com/download/desktop.

### 3.3. Create a New Virtual Machine (in VirtualBox)
1. Open VirtualBox.

2. Click "New" to create a new VM.

3. Name: ```Ubuntu 22.04 Ride App``` (or a similar descriptive name).

4. Folder: Choose a location on your host machine to store the VM files.

5. ISO Image: Browse and select the Ubuntu 22.04 LTS ISO you downloaded.

6. Type: ```Linux```

7. Version: ```Ubuntu (64-bit)```

8. Base Memory: Allocate at least ```4096 MB``` (4 GB) for better performance.

9. Processors: Allocate at least ```2 CPUs```.

10. Hard Disk: Create a virtual hard disk. Allocate at least ```25 GB``` (dynamically allocated is fine).

11. Click "Finish".

## 3.4. Install Ubuntu 22.04 in the VM
1. Select your newly created VM in VirtualBox and click "Start".

2. The VM will boot from the Ubuntu ISO.

3. Follow the on-screen instructions for installation:

    - Choose your language.

    - Select "Normal installation" and "Download updates while installing Ubuntu" (recommended).

    - Choose "Erase disk and install Ubuntu" (this refers to the virtual disk, not your host machine's disk).

    - Set up your timezone, keyboard layout, and create a user account (e.g., ```vboxuser```, with a strong password). Remember this username and password!

4. Once installation is complete, you'll be prompted to restart. Remove the installation medium (VirtualBox usually does this automatically).

## 3.5. Install VirtualBox Guest Additions (in Ubuntu VM)
This step is crucial for performance and usability.

1. After logging into your Ubuntu VM, go to the VirtualBox menu bar at the top of your host machine: ```Devices``` -> ```Insert Guest Additions CD Image....```

2. In your Ubuntu VM, a file manager window might pop up showing the contents of the "VBox_GAs_..." CD. If not, open the file manager and navigate to the "VBox_GAs_..." CD drive.

3. Right-click in the empty space within that file manager window and select "Open in Terminal".

4. In the terminal, run the installer script:
```
sudo sh ./VBoxLinuxAdditions.run
```
5. Troubleshooting "vboxuser is not in the sudoers file" (if it occurs):
If you get this error, it means your user doesn't have administrative privileges.

- Restart your Ubuntu VM.

- As it's booting, immediately press and hold the ```Shift``` key (or ```Esc```) to bring up the GRUB boot menu.

- Select "Advanced options for Ubuntu".

- Choose the option that says "Ubuntu, with Linux ... (recovery mode)".

- From the recovery menu, select "root Drop to root shell prompt".

- When prompted "Give root password for maintenance (or press Control-D to continue):", press Enter (or ```Ctrl+D``` if Enter doesn't work).

- At the root prompt (```#```), remount the filesystem as read-write:
```
mount -o remount,rw /
```
- Add your user (vboxuser) to the sudo group:
```
adduser vboxuser sudo
```
(Enter your vboxuser password if prompted).

6. Once sudo sh ./VBoxLinuxAdditions.run completes successfully, restart the VM:
```
sudo reboot
```
After reboot, you should have features like auto-resizing screen and shared clipboard.

##3.6. Update System and Install Python Tools (in Ubuntu VM)
1. Open a terminal (Ctrl+Alt+T).

2. Update your package lists:
```
sudo apt update
```
3. Upgrade installed packages:
```
sudo apt upgrade -y
```
4. Install pip and venv (Python virtual environment tool):
```
sudo apt install python3-pip python3-venv -y
```

## 3.7. Install MongoDB Community Edition (in Ubuntu VM)
1. Open a terminal.

2. Import the MongoDB public GPG key:
```
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor
```
3. Create a list file for MongoDB:
```
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
4. Reload local package database:
```
sudo apt update
```
5. Install MongoDB packages:
```
sudo apt install -y mongodb-org
```
6. Start MongoDB service:
```
sudo systemctl start mongod
```
7. Verify MongoDB status:
```
sudo systemctl status mongod
```
(Press ```q``` to exit the status view. You should see ```Active: active (running)```).

8. Enable MongoDB to start on boot (recommended):
```
sudo systemctl enable mongod
```
