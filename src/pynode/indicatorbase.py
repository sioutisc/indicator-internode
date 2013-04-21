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

import gconf
import appindicator as appi
import gtk

GCONF_ROOT = "/apps"

class IndicatorBase(appi.Indicator):
	def __init__(self,appid, icon_name, icon_theme_path):
		self.ind = appi.Indicator(appid, icon_name, appi.CATEGORY_APPLICATION_STATUS, icon_theme_path)
		self.gc = gconf.client_get_default()
		self.ind.set_status (appi.STATUS_ACTIVE)
		self.menu = gtk.Menu()
		self.ind.set_menu(self.menu)
		self.labels = {}
		self.cfgpath =  GCONF_ROOT + "/" + appid + "/"
		
	def get_root_menu(self):
		return self.menu
		
	def add_submenu(self,menu,label):
		item = gtk.MenuItem(label)
		submenu = gtk.Menu()
		item.set_submenu(submenu)
		menu.append(item)
		item.show()
		return submenu		

	def add_btn_menuitem(self,menu,label):
		item = gtk.MenuItem(label)
		menu.append(item)
		item.connect("activate",self.on_btn_menuitem_activated,label)
		item.show()
		return item

	def on_btn_menuitem_activated(self,menuitem,selection):
		print "IndicatorBase.on_cmd_menuitem_activated()"

	def add_chk_menuitem(self,menu,label,active):
		item = gtk.CheckMenuItem(label)
		if self.get_config(label) == None:
			item.set_active(active)
			self.set_config(label,str(active))
		else:
			item.set_active(self.get_config_bool(label))
		menu.append(item)
		item.connect("toggled",self.on_chk_menuitem_toggled,label)
		item.show()
		return item

	def on_chk_menuitem_toggled(self,menuitem,selection):
		self.set_config(selection, str(menuitem.get_active()))

	def add_lbl_menuitem(self,menu,lblid,lbltxt):
		item = gtk.MenuItem()
		lbl = gtk.Label(lbltxt)
		self.labels[lblid]=lbl
		item.add(lbl)
		item.show()
		menu.append(item)
		return item

	def set_lbl_menuitem(self,lblid,lbltxt):
		self.labels[lblid].set_text(lbltxt)
		
	def set_lbl_main(self,lbltxt):
		self.ind.set_label(lbltxt)
		
	def set_icn_main(self,icon):
		self.ind.set_icon(icon)

	def set_config(self,key,value):
		return self.gc.set_string(str(self.cfgpath)+key,value)
		
	def get_config(self,key):
		return self.gc.get_string(str(self.cfgpath)+key)	
	
	def get_config_bool(self,key):
		val = self.get_config(key)
		if val == "True":
			return True;
		return False
	