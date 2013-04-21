# =======================================================================
# Copyright 2013 Christos Sioutis <christos.sioutis@gmail.com>
# =======================================================================
# This file is part of indicator-internode.
#
# indicator-internode is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# indicator-internode is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with indicator-internode. 
# If not, see <http://www.gnu.org/licenses/>.
# =======================================================================

import gnomekeyring as gk
import gtk

KEYRING = "login"
DISPLAY_NAME = "indicator-internode"
#glib.set_application_name(DISPLAY_NAME)

class NotFoundException(Exception):
	pass

def load():
	item_keys = gk.list_item_ids_sync(KEYRING)
	for key in item_keys:
		item_info = gk.item_get_info_sync(KEYRING, key)
		if item_info.get_display_name().endswith(DISPLAY_NAME):
			item_info = gk.item_get_info_sync(KEYRING, key)
			keyring_attrs = gk.item_get_attributes_sync(KEYRING, key)
			return {"username":keyring_attrs["username"],"password":item_info.get_secret()}
	raise NotFoundException() 

def save(credentials):
	delete()		
	gk.item_create_sync(KEYRING, gk.ITEM_GENERIC_SECRET, credentials["username"]+"@"+DISPLAY_NAME,{"username":credentials["username"]}, credentials["password"], True)

def delete():
	item_keys = gk.list_item_ids_sync(KEYRING)
	for key in item_keys:
		item_info = gk.item_get_info_sync(KEYRING, key)
		if item_info.get_display_name().endswith(DISPLAY_NAME):
			item_info = gk.item_delete_sync(KEYRING, key)
	
def trigger_unlock():
	gk.item_create_sync(KEYRING, gk.ITEM_GENERIC_SECRET, "dummy",{"dummy":"dummy"}, "dummy", True)
	item_keys = gk.list_item_ids_sync(KEYRING)
	for key in item_keys:
		item_info = gk.item_get_info_sync(KEYRING, key)
		if item_info.get_display_name() == "dummy":
			item_info = gk.item_delete_sync(KEYRING, key)

def lock():
	gk.lock_sync(KEYRING)

def prompt():
	username = raw_input("Enter username: ")
	password = raw_input("Enter password: ")
	set(username,password)

def keyring_print(keyring):
	item_keys = gk.list_item_ids_sync(keyring)
	print 'Existing item Keys:',item_keys 
	for key in item_keys:
		item_info = gk.item_get_info_sync(keyring, key)
		print "\nItem number",key
		print "\tDisplay name:", item_info.get_display_name()
		print "\tPassword:", item_info.get_secret()
		print "\tAttributes:", gk.item_get_attributes_sync(keyring, key)

def dialog():	
	#base this on a message dialog
	dialog = gtk.MessageDialog(None,
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_QUESTION,
		gtk.BUTTONS_OK,
		None)
	dialog.set_markup('Please enter your internode <b>username</b> and <b>password</b>:')
	dialog.format_secondary_markup("This will be stored securely in your <i>login keyring</i>")
	# username 
	enUser = gtk.Entry()
	enUser.connect("activate", dialog_response, dialog, gtk.RESPONSE_OK)
	hbUser = gtk.HBox()
	hbUser.pack_start(gtk.Label("Username:"), False, 5, 5)
	hbUser.pack_end(enUser)	
	# password
	enPassw = gtk.Entry()
	enPassw.set_visibility(False) #shows *s instead of the text
	enPassw.connect("activate", dialog_response, dialog, gtk.RESPONSE_OK)
	hbPassw = gtk.HBox()
	hbPassw.pack_start(gtk.Label("Password:"), False, 5, 5)
	hbPassw.pack_end(enPassw)
	#setting up
	dialog.vbox.pack_end(hbPassw, True, True, 0)
	dialog.vbox.pack_end(hbUser, True, True, 0)
	dialog.show_all()
	dialog.run()
	#extracting info
	txtUser  = enUser.get_text()
	txtPassw = enPassw.get_text()
	dialog.destroy()
	return {"username":txtUser, "password":txtPassw}
	
def dialog_response(entry, dialog, response):
	dialog.response(response)

if __name__ == "__main__":
	try:
		print load()
	except AttributeError:
		print "Error: No credentials found"

