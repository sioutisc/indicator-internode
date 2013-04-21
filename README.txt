Installation instructions
=========================

1. indicator-internode requires python setuptools, to install it run the following command in a terminal

> sudo apt-get install python-setuptools

2. open a terminal and "cd" to directory where you extracted the package, then run the following command

> python setup.py install

you can now delete the download and extracted files

NOTE: The easy_install.sh script simply the above commands. The easy_uninstall.sh script deletes the installed files from the default locations

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

The application will now automatically start when the computer is rebooted
