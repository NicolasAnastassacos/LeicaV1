__author__ = 'nicolasanastassacos'

from setuptools import setup

APP = ['main.py']

setup(
	app = APP,
    author = 'Nicolas Anastassacos',
	options = {
		'py2app': {
			'includes': ['PySide.QtCore', 'PySide.QtGui', 'PySide.QtWebKit', 'PySide.QtNetwork'],
		}
	},
	data_files = [],
	setup_requires = ['py2app'],
)

'''
from cx_Freeze import setup, Executable

setup(
    name = "testingGUI",
    version = "1.0",
    description = "SpiraGUI",
    executables = [Executable("main.py")]

    otool -L /Library/Python/2.7/site-packages/PySide/QtCore.so
    install_name_tool -change "<path listed for libpyside above>" "<actual path to libpyside" /Library/Python/2.7/site-packages/PySide/QtCore.so
    )
'''