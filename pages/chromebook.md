---
layout: page
title: Running Linux on a Chromebook
description: chromebook, hardware requirements
---

I got the Acer Chromebook 14 ($300) because it has an Intel chip, 32GB disk space and 4GB RAM.

installing Linux
----------------

I used Crouton to instal Linux on it. See
[this](https://www.linux.com/learn/how-easily-install-ubuntu-chromebook-crouton)
and [this](https://github.com/dnschneid/crouton).
I choose the light Ubuntu 12.04 LTS (also called "precise") with Xfce4.

Once in Ubuntu, the first issue was the mouse. It was barely working, I had to press
really hard. In the terminal I did this to fix the sensitivity of the touchpad:
`synclient FingerLow=1 FingerHigh=5`.

I updated the system just to make sure:
`sudo apt-get update`, then `sudo apt-get upgrade` and then `sudo apt-get install`.
and then installed a bunch of things.

install git
-----------
for version control. Very easy: `sudo apt-get install git` in the terminal.

todo: install gedit
-------------
first check if it shipped with Ubuntu already. Probably so.

todo: instal Nautilus
---------------

Nautilus is a file browser that makes it really easy to connect to a server
(like the stat servers), access remote files and edit these files remotely without
having to store them locally.


install Atom
------------
great text editor: see [here](https://github.com/atom/atom) and
[here](https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md).
It has a bunch of dependencies.

- First I tried the easy way. I downloaded Atom v1.8.0
[here](https://github.com/atom/atom/releases/download/v1.8.0/atom-amd64.deb) and ran
`sudo dpkg --install atom-amd64.deb`. But it complained about unmet dependencies.

- Next I tried building the package from source, using instructions
[here](https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md),
which start by getting dependencies with this:
`sudo apt-get install build-essential git libgnome-keyring-dev fakeroot`
but their own dependencies were not met, like `g++`, `make` and `dpkg-dev`.
So I ran this to get them: `sudo apt-get -f install` and then again
`sudo apt-get install build-essential libgnome-keyring-dev fakeroot`.  
I ran another update of the system: `sudo apt-get update` then got `curl`:
`sudo apt-get install curl`.
Another of `atom`'s dependency is `Node.js`:
`curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -` then
`sudo apt-get install -y nodejs`.  
Then I followed the build instructions to build `atom`, in a new directory that I called
`apps`: `mkdir apps` then `cd apps` then `git clone https://github.com/atom/atom` etc.
The build failed in the end.

- So I retried the installation using the pre-built package downloaded earlier,
hoping that the dependencies that were missing earlier would now be taken care of:
`sudo dpkg --install ~/Downloads/atom-amd64.deb`. This time, it worked.

I could finally launch my text editor by doing `atom`.

tips
----
- at boot up: skip the (scary) developer mode message by pressin Ctrl+D.
