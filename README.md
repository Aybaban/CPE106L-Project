# Accessible Transportation Scheduler

## Download [Python](https://www.python.org/downloads/) by clicking this link
All information came from [Real Python](https://realpython.com/installing-python/#macos-how-to-install-python-from-homebrew)

# Windows: How to Check or Get Python

In this section, you’ll learn to check whether Python is installed on your Windows operating system (OS) and which version you have. You’ll also explore three installation options that you can use on Windows.


Checking the Python Version on Windows
To check whether you already have Python on your Windows machine, open a command-line application like PowerShell or the Windows Terminal.

Follow the steps below to open PowerShell on Windows:

```
Press the Win key.
Type PowerShell.
Press Enter.
```
# Windows: How to Install Python Using the Official Installer

For developers needing a full-featured Python development environment, installing from the official Python installer is recommended. It offers more customization and control over the installation process.

In this section, you’ll go through the necessary steps to install Python using the official installer from Python.org.


## Step 1: Download the Official Python Installer
Follow the steps below to download the official Python installer from the Python.org site:


1. Open your browser and navigate to the downloads page for Windows on Python.org.

2. Under the Python Releases for Windows heading, click the link for the Latest Python 3 Release - Python 3.x.z.

3. Scroll to the bottom and select either Windows installer (64-bit) or Windows installer (32-bit).

When you finish downloading the installer, then you can move on to the next step.

## Step 2: Run the Python Installer
Once you’ve chosen and downloaded an installer, run it by double-clicking on the file.

Windows Python Installer
There are four important things to notice about this dialog box:

1. The default install path is in the AppData/ directory of the current Windows user.
2. The Customize installation button allows you to customize the installation location and some additional features, including installing pip and IDLE.
3. The Use admin privileges when installing py.exe allows every user on the machine access the py.exe launcher.
4. The Add python.exe to PATH checkbox is also unchecked by default. There are several reasons that you might not want Python on PATH, so make sure you understand the implications before you check this box.

As you can conclude, the official Python installer gives you granular control over the installation process on Windows.

```
Note: If you want the python command to work on your Windows machine, then it’s recommended that you activate the PATH check box.
```

Use the options in the dialog box to customize the installation to meet your needs. Then click Install. That’s it! You now have the latest version of Python 3 on your Windows machine!

If you’re interested in where the installation is located, then you can use the where.exe command in PowerShell:

```
PS> where.exe python
C:\Users\realpython\AppData\Local\Microsoft\WindowsApps\python.exe
```

Note that the where.exe command will work only if Python has been installed for your user account.


# Linux: How to Check or Get Python

In this section, you’ll learn how to check which version of Python, if any, is on your Linux computer. You’ll also learn about the installation options to get the latest Python on Linux systems.

Checking the Python Version on Linux
Most Linux distributions come with Python installed by default. In most cases, the installed version won’t be the latest Python. To find out which version of Python you have on Linux, open a terminal window and run the following command:

```
$ python3 --version
```

If you have Python on your machine, then this command will respond with a version number. Instead of --version, you can use the shorter -V switch:

```
$ python3 -V
```
Either of these switches will give you the version number of the Python installation that the command is associated with. If your current version is outdated, you’ll want to get the latest version of Python.

# Linux: How to Build Python From Source Code
You’ll have at least three reasons to choose to build Python from source code:

1. You need to install the latest version of Python or a version unavailable on your distribution’s repository.
2. You need to control how Python is compiled, such as when you want to lower the memory footprint on embedded systems.
3. You want to try out pre-release versions to explore new features.

You can run the steps in the following sections to complete the installation on your Linux machine.

## Step 1: Download the Python Source Code
To start, you need to clone the cpython repository from GitHub or get the Python source code from Python.org. If you go to the downloads page, then you’ll find the latest source for Python 3 at the top.

When you select the latest Python version, you’ll see a Files section at the bottom of the page. Select Gzipped source tarball and download it to your machine.

If you prefer to use your command line, then you can use wget to download the file to your current directory:

```
$ wget https://www.python.org/ftp/python/3.x.z/Python-3.x.z.tgz
```

For this command to work, you must specify the version to download. When the tarball finishes downloading, there are a few things you’ll need to do to prepare your system for building Python.

## Step 2: Prepare Your System for Building Python
There are a few distro-specific steps involved in building Python from source. The goal of this section is to prepare your system for building Python. Below, you’ll find specific steps for some popular Linux distributions.

## Ubuntu, Debian, and Linux Mint
First, update the list of available packages and upgrade them using the following commands:

```
$ sudo apt update
$ sudo apt upgrade
```

Note that because you’re using the sudo command, you’ll be prompted to provide your root password.

Next, make sure you have all of the build requirements installed:

```
$ sudo apt install -y make build-essential libssl-dev zlib1g-dev \
       libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
       libncurses5-dev libncursesw5-dev xz-utils tk-dev
```

It’s okay if you already have some of these requirements installed on your system. You can execute the above commands, and any existing packages will be skipped.




# macOS: How to Check or Get Python
Python comes preinstalled on macOS. However, the installed version may not be the most recent one. To take advantage of Python’s latest features, you’ll need to download and install newer versions alongside the system one.

Checking the Python Version on a macOS
To check which Python version you have on your Mac, open a command-line application like Terminal.

Here’s how you open Terminal on macOS:

```
Press the Cmd+Space keys.
Type Terminal.
Press Enter.
```

Alternatively, you can open Finder and navigate to Go → Utilities → Terminal.

With the command line open, type in the following commands:

```
$ python3 --version
```

This command should respond with a version number. Alternatively, you can use the shorter -V switch, which has the same effect.

In practice, you’d want to get the latest version of Python if none of the above commands returns a version number or if you have a version of Python 3 that isn’t the latest available. Now, you can read through the following sections to learn about the different options for installing Python on macOS.

# macOS: How to Install Python From Homebrew

The Homebrew package manager is another good option for installing Python on macOS. You can install Python using the Homebrew package manager in two steps, but first, you need to be aware of some limitations of the Python package on Homebrew.

The Python distribution available on Homebrew doesn’t include the Tcl/Tk dependency, which is required by the Tkinter module. Tkinter is the standard library module for developing graphical user interfaces in Python and is an interface for the Tk GUI toolkit, which isn’t part of Python.

Homebrew doesn’t install the Tk GUI toolkit dependency. Instead, it relies on an existing version installed on your system. The system version of Tcl/Tk may be outdated or missing entirely and could prevent you from using Tkinter.

Finally, note that the Python distribution on Homebrew isn’t maintained by the Python Software Foundation and could change at anytime.

## Step 1: Install the Homebrew Package Manager

If you already have Homebrew installed on your macOS system, then you can skip this step. If you don’t have it installed, then use the following procedure:

1. Open a browser and navigate to http://brew.sh/.
2. Copy the installation command under the Install Homebrew heading.
3. Open a terminal window and paste the command, then press Enter.
4. Enter your macOS user password when prompted.

Depending on your Internet connection speed, the process may take a few minutes to download all of Homebrew’s required files. Once the installation is complete, you’ll be back at the shell prompt in your terminal window.

Note: If you’re doing this on a fresh install of macOS, you may get a pop-up alert asking you to install Apple’s command line developer tools. These tools are necessary for installation, so you can confirm the dialog box by clicking Install.

After the developer tools are installed, you’ll need to press Enter to continue installing Homebrew.

Now that Homebrew is installed, you’re ready to install Python.

## Step 2: Install Python With Homebrew
Installing Python with the Homebrew package manager is now as straightforward as running the following command:

```
$ brew install python
```

This command will download, install, and set up the latest version of Python on your machine. You can make sure everything went correctly by testing if you can access Python from the terminal. If you get an error message, then go through the install steps again to make sure you have a working installation.


Project of:
- De Guzman, Franz Ivan.
- Sean Cruz
- Sun Jung Yun
