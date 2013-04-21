indicator-internode
===================

Ubuntu unity indicator to monitor internet usage for the Internode ISP

Latest release
==============

https://github.com/sioutisc/indicator-internode/archive/v12.10.1.zip

Installation instructions
=========================

1. indicator-internode requires python setuptools, to install it run the following command in a terminal

> sudo apt-get install python-setuptools

2. open a terminal and "cd" to directory where you extracted the package, then run the following command

> python setup.py install

you can now delete the download and extracted files

NOTE: The easy_install.sh script simply executes the above commands. Conversely, the easy_uninstall.sh script deletes installed files from their default locations

Running the application
=======================

open a terminal and run the following command

> indicator-internode

Running on startup
==================

1. click "Dash Home" on the top-right of the desktop
2. type "startup" in the search field
3. select "Startup Applications" from the applications
4. click "Add" button and put the following details in the dialog
   Name: indicator-internode
   Command: indicator-internode
   Comment: Internode usage indicator 
5. Click "Add" button

This application will now automatically start when the computer is rebooted

NOTE: This application uses the Gnome Keyring to securely store passwords. This works best when using the login screen on startup (ie. entering a username/password to log into your system) because that also unlocks the keyring. When using the "auto-login" feature your system will boot straight into the desktop without unlocking the keyring. This application will then trigger an unlock of the keyring and you will immediately get (maybe annoyingly) a password dialog box every time you log in.


