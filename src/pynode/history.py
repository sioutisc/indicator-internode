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

def barchart(title,data):
	barchart = bar_chart.BarChart()
	barchart.title.set_text(title)
	barchart.grid.set_visible(True)
	barchart.grid.set_line_style(pygtk_chart.LINE_STYLE_DOTTED)
	barchart.set_mode(bar_chart.MODE_HORIZONTAL)
	
	for bar_info in data:
	    bar = bar_chart.Bar(*bar_info)
	    #bar.set_corner_radius(4)
	    barchart.add_bar(bar)

	window = gtk.Window()
	window.connect("destroy", gtk.main_quit)
	window.add(barchart)
	window.resize(800,400)
	window.show_all()

if __name__ == "__main__":
        data = [('wheat', 276, 'Wheat'),
                     ('oat', 52, 'Oat'),
                     ('white', 652, 'White'),
                     ('sour', 65, 'Sourdough'),
                     ('raisin', 120, 'Raisin'),
                    ]
        barchart('Loaves of Bread Made',data)
        gtk.main()
