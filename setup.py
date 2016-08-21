from setuptools import setup,find_packages

setup(
	name		= 'indicator-internode',
	version		= '12.10.1',
	description	= 'A ubuntu unity indicator to monitor internet usage for the internode ISP',
	author		= 'Christos Sioutis',
	author_email	= 'christos.sioutis@gmail.com',
	url		= 'TBA',
	packages	= ['pynode', 'pygtk_chart'],
	package_dir	= {'pynode':'src/pynode', 'pygtk_chart':'src/pygtk_chart'},
	package_data	= {'pynode':['icons/*.svg'], 'pygtk_chart':['data/tango.color']},
	include_package_data = True,
	scripts		= ['src/indicator-internode'],
)
