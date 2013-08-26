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

import gtk
import pygtk

import pygtk_chart
from pygtk_chart import bar_chart

import credentials
import nodeapi

def month(app,history_data):
	daily_data = []
	for day in history_data[-31:]:
		daily_data.append((day["day"],int(float(day["used"])/1000000),day["day"]))
	barchart(app,"Internet Usage Last 31 Days (MB)",daily_data)

def year(app,history_data):
	monthly_data = {}
	for day in history_data:
		try:
			monthly_data[day["day"][:7]] = monthly_data[day["day"][:7]] + float(day["used"])
		except KeyError:
			monthly_data[day["day"][:7]] = float(day["used"])
	monthly_data_sorted = sorted((k,int(v/1000000000),k) for (k,v) in monthly_data.items())
	barchart(app,"Monthly Internet Usage (GB)",monthly_data_sorted)


def barchart(app,title,data):
	barchart = bar_chart.BarChart()
#	barchart.title.set_text(title)
	barchart.grid.set_visible(True)
	barchart.grid.set_line_style(pygtk_chart.LINE_STYLE_DOTTED)
	barchart.set_mode(bar_chart.MODE_HORIZONTAL)
	
	for bar_info in data:
	    bar = bar_chart.Bar(*bar_info)
	    #bar.set_corner_radius(4)
	    barchart.add_bar(bar)

	window = gtk.Window()
	window.set_title(title + " - " + app)
	window.add(barchart)
	window.resize(800,400)
	window.show_all()

