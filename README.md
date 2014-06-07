indicator-internode
===================

Ubuntu unity indicator to monitor internet usage for the Internode ISP

Latest release
==============

https://github.com/sioutisc/indicator-internode/archive/v14.04.1.zip

The version numbers follow the particular ubuntu release on which the application
was tested. It may still work with a newer release if the underlying API is compatible.

Dependencies
============

Starting with ubuntu 13.10 the python bindings for appindicator are not installed
by default. It is necessary for people to manually install "python-appindicator"
package using the software center before this application with work.

Installation instructions
=========================

NOTE: You can also run the application without installing it, simply execute the "indicator-internode" command from within the "src" directory.

1. indicator-internode uses the setuptools library to automate installation. This library needs to be
manually installed using the following command in a terminal

> sudo apt-get install python-setuptools

2. open a terminal and "cd" to directory where you extracted the package, then run the following command

> python setup.py install

you can now delete the download and extracted files

NOTE: The simple_install.sh script simply executes the above commands. Conversely, the simple_uninstall.sh script deletes installed files from their default locations

Running the application
=======================

Just open a terminal and run the following command

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


