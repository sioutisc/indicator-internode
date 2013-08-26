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
import urllib2
import time
import datetime
import sys
import logging
import logging.handlers
from calendar import monthrange

from indicatorbase import *
import nodeapi
import credentials
import history

from gnomekeyring import IOError as GK_IOError
from gnomekeyring import CancelledError as GK_CancelledError

import ssl
import os

APP_ID = "indicator-internode"
APP_VER = "12.10.1"
APP_ID_VER=APP_ID+"-"+APP_VER
APP_LOG="/tmp/"+APP_ID+".log"

ICON_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icons')

ICON_NEUTRAL		= "white"
ICON_OK			= "green"
ICON_WARNING		= "yellow"
ICON_CRITICAL		= "red"
ICON_DEFAULT 		= ICON_NEUTRAL

THRESHOLD_WARNING 	= 0.75
THRESHOLD_CRITICAL	= 0.5

UPDATE_RETRY_DELAY 	= 2000 # 2secs
UPDATE_DELAY 		= 60000 * 5  # 5mins

INTERVAL_15M 	= "15m"
INTERVAL_30M 	= "30m"
INTERVAL_1HR 	= "1hr"
INTERVAL_12HR 	= "12hr"
INTERVALS = {INTERVAL_15M: 15, INTERVAL_30M: 30, INTERVAL_1HR: 60, INTERVAL_12HR:720}

DEFAULT_LOGGING = logging.INFO

class NodeInd(IndicatorBase):
	
	############ initialisation ##########################################
	def __init__(self):
		IndicatorBase.__init__(self,APP_ID,ICON_DEFAULT,ICON_PATH)
		self.init_logging()
		self.logger.debug("init")
		self.credentials = None
		self.service = None
		self.usage = None
		self.deadline = datetime.datetime.now()
		self.history_data = None
		self.history_deadline = self.deadline
		update_interval = INTERVALS[INTERVAL_1HR]
		self.init_menu()
		self.init_interval()
		#reset deadline for first update
		self.deadline = datetime.datetime.now()

	def init_logging(self):
		self.logger = logging.getLogger(APP_ID)
		ftr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		#fh = logging.FileHandler(APP_LOG)
		#fh.setFormatter(ftr)
		#self.logger.addHandler(fh)
		sh = logging.StreamHandler(sys.stdout)
		sh.setFormatter(ftr)
		self.logger.addHandler(sh)
		self.logger.setLevel(DEFAULT_LOGGING)
		
	def init_menu(self):
		self.set_lbl_main("OFF")
		self.suppress_toggles = False		
		menu = self.get_root_menu()
		self.add_lbl_menuitem(menu,"data", "----------")
		self.add_lbl_menuitem(menu,"budget", "----------")
		self.add_chk_menuitem(menu,"Colour",False)
		submenu = self.add_submenu(menu,"Interval")
		self.interval_options = []
		self.interval_options.append(self.add_chk_menuitem(submenu,INTERVAL_15M,False))
		self.interval_options.append(self.add_chk_menuitem(submenu,INTERVAL_30M,False))
		self.interval_options.append(self.add_chk_menuitem(submenu,INTERVAL_1HR,True))
		self.interval_options.append(self.add_chk_menuitem(submenu,INTERVAL_12HR,False))
		self.add_btn_menuitem(menu,"Update Now")
		history = self.add_submenu(menu,"History")
		self.add_btn_menuitem(history,"Month")
		self.add_btn_menuitem(history,"Year")
		self.add_btn_menuitem(menu,"Account")

	def init_interval(self):
		for item in self.interval_options:
			if item.get_active():
				self.set_interval(item.get_label())

	############ user interface ##########################################
	
	def on_btn_menuitem_activated(self,menuitem,selection):
		if selection == "Update Now":
			self.deadline = datetime.datetime.now()
			self.update()
			return

		if selection == "Account":
			c = credentials.dialog()
			if len(c["username"]) > 0 and len(c["password"]) > 0:
				self.credentials = None
				self.service = None
				self.usage = None
				# do twice incase user unlocked keyring on prompt
				for index in range(2):
					try:
						credentials.save(c)
						self.credentials = c
						self.logger.debug(str(self.credentials))
						self.logger.info("credentials updated")
						self.deadline = datetime.datetime.now()
						self.update()
						return
					except GK_IOError:
						try:
							credentials.trigger_unlock()
						except GK_CancelledError, e:
							pass
			return

		if selection == "Month":
			self.update_history()
			history.month(APP_ID,self.history_data)
			return

		if selection == "Year":
			self.update_history()
			history.year(APP_ID,self.history_data)
			return

	def on_chk_menuitem_toggled(self,menuitem,selection):
		if self.suppress_toggles == True:
			return 
		self.set_config(selection, str(menuitem.get_active()))
		if selection == "Colour":
			self.update_labels()
		else:
			self.set_interval_menu(menuitem)

	def set_interval_menu(self,menuitem):
		self.suppress_toggles = True
		for item in self.interval_options:
			if item == menuitem:
				item.set_active(True)
				self.set_config(item.get_label(),str(True))
				self.set_interval(item.get_label())
			else:
				item.set_active(False)
				self.set_config(item.get_label(),str(False))
		self.suppress_toggles = False

	def set_interval(self,interval):
		self.logger.debug("interval set to "+interval)
		self.update_interval = INTERVALS[interval]
		now = datetime.datetime.now()
		self.deadline = now + datetime.timedelta(minutes=self.update_interval)
		self.logger.info( "next update "+str(self.deadline))

	############ updating ##########################################

	def update(self):
		try:
			self.update_credentials()
			self.logger.debug("update - "+str(self.credentials))
			self.update_service()
			self.logger.debug("update - "+str(self.service))
			self.update_usage()
			self.logger.debug("update - "+str(self.usage))
			self.logger.info("next update "+str(self.deadline))
			gtk.timeout_add(UPDATE_DELAY,self.update)
		except RetryException, e:
			self.logger.warning(str(e))
			self.logger.debug("retrying")
			gtk.timeout_add(UPDATE_RETRY_DELAY,self.update)
		except AbortException, e:
			self.logger.debug("aborting")
			self.reset_ui(str(e))
	
	def update_credentials(self):
		if self.credentials == None:
			try:
				self.logger.debug("credentials get")
				self.credentials = credentials.load()
				self.logger.info("credentials retrieved")
			except credentials.NotFoundException:
					self.logger.error("credentials not found")
					raise AbortException("OFF")
			except GK_IOError, e:
				try:
					credentials.trigger_unlock()
					raise RetryException("keyring is locked, trigger unlock")
				except GK_CancelledError:
					self.logger.error("keyring is locked")
					raise AbortException("KEYR")

	def update_service(self):
		if self.credentials != None and self.service == None:
			try:
				self.logger.debug("service details get")
				self.service = nodeapi.services(APP_ID_VER,self.credentials)[0]
				self.logger.info("service details retrieved")
			except urllib2.HTTPError, e:
				if e.code == 401:
					self.logger.error("authentication rejected")
					raise AbortException("AUTH")
				else:
					raise RetryException(str(e))
			except ssl.SSLError, e:
				self.logger.warning(str(e))
				raise RetryException()			
		
	def update_usage(self):
		if self.credentials != None and self.service != None:
			now = datetime.datetime.now()
			if now > self.deadline:
				try:
					self.logger.debug("usage details get")
					self.usage = nodeapi.usage(APP_ID_VER,self.credentials,self.service)
					self.logger.info("usage details retrieved")
					self.update_labels()
					self.deadline = now + datetime.timedelta(minutes=self.update_interval)
				except urllib2.HTTPError, e:
					self.deadline = now
					raise RetryException(str(e))
				except ssl.SSLError, e:
					self.logger.warning(str(e))
					raise RetryException()			

	def update_labels(self):
		if self.usage == None:
			return
		used = float(self.usage["used"])
		quota = float(self.usage["quota"])
		rollover_time = time.strptime(self.usage["rollover"], "%Y-%m-%d")
		rollover_date  = datetime.date.fromtimestamp(time.mktime(rollover_time))
			
		txtMain =  "%.1f" % (used / quota * 100)
		self.set_lbl_main(txtMain+"%");

		txtData =  "%.1fGB" % nodeapi.bytes_to_gb(used) + " used of %i" % nodeapi.bytes_to_gb(quota)
		self.set_lbl_menuitem("data", txtData)

		now = datetime.date.today()
		delta = rollover_date - now
		days_remaining = delta.days
		days_in_month = monthrange(now.year,now.month)[1]
		daily_budget = quota / days_in_month
		budget = daily_budget + ((days_in_month-days_remaining) * daily_budget)
		daily_budget_remaining = (quota-used)/days_remaining

		if budget > used:
			txtBudg =  "%.1fGB" % nodeapi.bytes_to_gb(budget-used) + " under budget"
			self.set_lbl_menuitem("budget", txtBudg)
			self.update_icon(ICON_OK)
		elif budget < used:
			txtBudg = "%.1fGB" % nodeapi.bytes_to_gb(used-budget) + " over budget"
			self.set_lbl_menuitem("budget", txtBudg)
			if daily_budget_remaining / daily_budget < THRESHOLD_CRITICAL:
				self.update_icon(ICON_CRITICAL)
			elif daily_budget_remaining / daily_budget < THRESHOLD_WARNING:
				self.update_icon(ICON_WARNING)
		else:
			self.set_lbl_menuitem("budget", "Exactly on budget")
			self.update_icon(ICON_OK)
		
	def update_icon(self,icon):
		if self.get_config_bool("Colour"):
			self.set_icn_main(icon)
		else:
			self.set_icn_main(ICON_DEFAULT)

	def update_history(self):
		# history is only updated when usage details deadline changes
		if self.history_data != None and self.history_deadline == self.deadline:
			self.logger.info("using current history details")
			return
		try:
			self.logger.debug("history details get")
			self.history_data = nodeapi.history(APP_ID_VER,self.credentials,self.service)
			self.history_deadline = self.deadline
			self.logger.info("history details retrieved")
		except Exception, e:
			self.logger.error(str(e))

	def reset_ui(self,lblMain="OFF"):
		self.set_lbl_main(lblMain)
		self.set_lbl_menuitem("data", "----------")
		self.set_lbl_menuitem("budget", "----------")
		self.set_icn_main(ICON_DEFAULT)

class RetryException(Exception):
	pass

class AbortException(Exception):
	pass

#if __name__ == "__main__":
def start():
	ni = NodeInd()
	ni.set_lbl_main("WAIT")
	gtk.timeout_add(UPDATE_RETRY_DELAY,ni.update)
	gtk.main()
