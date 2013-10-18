indicator-internode
===================

Ubuntu unity indicator to monitor internet usage for the Internode ISP

Latest release
==============

https://github.com/sioutisc/indicator-internode/archive/v13.10.1.zip

The version numbers follow the particular ubuntu release on which the application
was tested. It may still work with a newer release if the underlying API is compatible.

Installation instructions
=========================

1. Starting with ubuntu 13.10 the python bindings for appindicator are not installed by default.
It is necessary to manually install "python-appindicator" as follows:

> sudo apt-get install python-appindicator

2. The application can run without installing it, simply execute the "indicator-internode"
command from within the "src" directory. It can also be installed using the setuptools library
which needs to be installed first.

> sudo apt-get install python-setuptools

2. open a terminal and "cd" to directory the package is extracted, then run the following command

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


