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

# This code is based on nodeutil.py, it has been simplified and made state-less
# https://github.com/AntiSol/nodeutil by Dale Maggee and others

import time
import datetime
import urllib2
import base64
from xml.dom import minidom

# for simplicity matches intenode api version
NODEAPI_VERSION="1.5"
NODEAPI_HOST = "https://customer-webtools-api.internode.on.net"
HTTP_TIMEOUT = 5

def services(app,credentials):
	services = []
	dom = http_request(app,credentials,"/api/v"+NODEAPI_VERSION+"/")
	for node in dom.getElementsByTagName('service'):
		svc = dict(node.attributes.items())
		svc["id"] = get_node_data(node)
		services.append(svc)
	return services

def usage(app,credentials,service):
	dom = http_request(app,credentials,"%s/usage" % service['href'])
	node = dom.getElementsByTagName('traffic')[0]
	usage = dict(node.attributes.items())
	usage["used"] = get_node_data(node)
	return usage

def history(app,credentials, service):
	history = []
	dom = http_request(app,credentials,"%s/history" % service['href'])
	for node in dom.getElementsByTagName('usage'):
		day = node.childNodes[0]
		usage = dict(day.attributes.items())
		usage["used"] = get_node_data(day)
		usage["day"] = node.getAttribute("day")
		history.append(usage)
	return history

def service_info(app,credentials,service):
	info = {}
	dom = http_request(app,credentials,"%s/service" % service['href'])
	svc = dom.getElementsByTagName('service')[0]
	for node in svc.childNodes:
		info[node.tagName] = get_node_data(node)
		if node.hasAttributes():
			for attr in node.attributes.items():
				info[node.tagName+"-"+attr[0]]=attr[1]
	return info

def http_auth_string(credentials):
	base64string = base64.encodestring("%s:%s" % (credentials["username"], credentials["password"]))[:-1]
	return "Basic %s" % base64string

def http_request(app,credentials,path):
	request = urllib2.Request("%s%s" % (NODEAPI_HOST, path))
	request.add_header('User-Agent', app+"-nodeapi-"+NODEAPI_VERSION)
	request.add_header('Authorization', http_auth_string(credentials))
	result = urllib2.urlopen(request,None,HTTP_TIMEOUT)
	return minidom.parse(result)

def get_node_data(node):
	text = ""
	for node in node.childNodes:
		if node.nodeType == node.TEXT_NODE:
			text = text + node.data
	return text

def parse_date(date):
	datetuple = time.strptime(date, '%Y-%m-%d')
	return datetime.date(datetuple[0], datetuple[1], datetuple[2])

def get_date_difference(rollover):
	diff = parse_date(rollover) - datetime.date.today()
	return diff.days

def bytes_to_gb(b):
	return b / 1000000000
