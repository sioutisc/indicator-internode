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
# Licensse along with indicator-internode. 
# If not, see <http://www.gnu.org/licenses/>.
# =======================================================================

import gconf
import appindicator as appi
import gtk

GCONF_ROOT = "/apps"

class IndicatorBase(appi.Indicator):
	def __init__(self,strAppId, strIconName, strIconThemePath):
		self.ind = appi.Indicator(strAppId, strIconName, appi.CATEGORY_APPLICATION_STATUS, strIconThemePath)
		self.gc = gconf.client_get_default()
		self.ind.set_status (appi.STATUS_ACTIVE)
		self.menus = {"root":gtk.Menu()}
		self.labels = {}
		self.cfgpath =  GCONF_ROOT + "/" + strAppId + "/"

	def finalize_menu(self):
		self.ind.set_menu(self.menus["root"])

	def add_submenu(self,strParent,strLabel):
		item = gtk.MenuItem(strLabel)
		submenu = gtk.Menu()
		item.set_submenu(submenu)
		self.menus[strLabel] = submenu
		self.menus[strParent].append(item)
		item.show()
		return submenu

	def add_btn_menuitem(self,strParent,strLabel):
		item = gtk.MenuItem(strLabel)
		self.menus[strParent].append(item)
		item.connect("activate",self.on_btn_menuitem_activated,strLabel)
		item.show()
		return item

	def on_btn_menuitem_activated(self,gtkMenuItem,strSelection):
		print "IndicatorBase.on_cmd_menuitem_activated selection="+strSelection

	def add_chk_menuitem(self,strParent,strLabel,boolActive):
		item = gtk.CheckMenuItem(strLabel)
		if self.get_config(strLabel) == None:
			item.set_active(boolActive)
			self.set_config(strLabel,str(boolActive))
		else:
			item.set_active(self.get_config_bool(strLabel))
		self.menus[strParent].append(item)
		item.connect("toggled",self.on_chk_menuitem_toggled,strLabel)
		item.show()
		return item

	def on_chk_menuitem_toggled(self,gtkMenuItem,strSelection):
		self.set_config(strSelection, str(gtkMenuItem.get_active()))

	def add_separator(self,strParent):
		separator = gtk.SeparatorMenuItem()
		separator.show()
		self.menus[strParent].append(separator)

	def add_lbl_menuitem(self,strParent,strID,strLabel):
		item = gtk.MenuItem()
		lbl = gtk.Label(strLabel)
		self.labels[strID] = lbl
		item.add(lbl)
		item.show()
		self.menus[strParent].append(item)
		return item

	def set_lbl_menuitem(self,strID,strLabel):
		self.labels[strID].set_text(strLabel)
		
	def set_lbl_main(self,strLabel):
		self.ind.set_label(strLabel)
		
	def set_icn_main(self,strIconPath):
		self.ind.set_icon(strIconPath)

	def set_config(self,strKey,strValue):
		return self.gc.set_string(str(self.cfgpath)+strKey,strValue)
		
	def get_config(self,strKey):
		return self.gc.get_string(str(self.cfgpath)+strKey)	
	
	def get_config_bool(self,strKey):
		val = self.get_config(strKey)
		if val == "True":
			return True;
		return False
	
