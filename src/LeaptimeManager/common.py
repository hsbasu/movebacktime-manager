# Copyright (C) 2021-2023 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
# This file is part of LeapTime Manager.
#
# LeapTime Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LeapTime Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LeapTime Manager. If not, see <http://www.gnu.org/licenses/>
# or write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA..
#
# Author: Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#

# import the necessary modules!
import configparser
import getpass
import gettext
import glob
import locale
import logging
import os
import string

from random import choice


# i18n
APP = 'leaptime-manager'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext


## Setup logfile
def create_logfile():
	logpath = '/tmp/'
	dlimitter = '_'
	username = getpass.getuser()
	random_code =  ''.join(choice(string.digits) for _ in range(4))
	if len(glob.glob(logpath+APP+dlimitter+username+'*')) ==0:
		logfile = logpath + APP + dlimitter + username + dlimitter + random_code + '.log'
	else:
		logfile = glob.glob(logpath+APP+dlimitter+username+'*')[0]
	
	return logfile
# Set the log filename
LOGFILE = create_logfile()

# logger
module_logger = logging.getLogger('LeaptimeManager.common')

description = _("Aiming to be an all-in-one, friendly to new-users, GUI based backup manager for Debian/Ubuntu based systems.")

# get version
version_file = os.path.abspath(os.path.dirname(__file__))+'/VERSION'
__version__ = open(version_file, 'r').readlines()[0]

# Constants
CONFIG_DIR = os.path.expanduser('~/.config/leaptime-manager/')
CONFIG_FILE = os.path.join(CONFIG_DIR+'config.cfg')
UI_PATH = os.path.dirname(os.path.realpath(__file__)) + "/ui/"

class LTM_backend():
	"""
	Common functions used by other modules.
	"""
	def __init__(self):
		module_logger.debug(_("Initializing backend."))
		if os.path.exists(CONFIG_DIR):
			module_logger.debug(_("Configuration directory exists. Nothing to do."))
		else:
			module_logger.debug(_("Creating configuration directory."))
			os.makedirs(CONFIG_DIR)
		
		self.config = configparser.ConfigParser()
		self.save_config()
		self.load_config()
	
	def load_config(self):
		"""Loads configurations from config file.
		
		Tries to read and parse from config file.
		If the config file is missing or not readable,
		then it triggers default configurations.
		"""
		
		module_logger.debug(_("Loading existing configurations."))
		self.config.read(CONFIG_FILE)
		self.app_backup_db = self.config['db']['app-db']
		self.userdata_db = self.config['db']['userdata-db']
		self.create_db_files()
	
	def save_config(self):
		# Save main config file
		if os.path.exists(CONFIG_FILE):
			module_logger.debug(_("Configuration file exists. Validating configurations."))
			self.validate_config
		else:
			module_logger.debug(_("Creating configuration files."))
			self.config['db'] = {
				'app-db': CONFIG_DIR+"apps_backup.json",
				'userdata-db': CONFIG_DIR+"userdata_backups.json"
			}
			with open(CONFIG_FILE, 'w') as f:
				self.config.write(f)
	
	def create_db_files(self):
		# create app backups database file
		if not os.path.exists(self.app_backup_db):
			with open(self.app_backup_db, 'w') as f:
				pass
		# create user data backups database file
		if not os.path.exists(self.userdata_db):
			with open(self.userdata_db, 'w') as f:
				pass
	
	def validate_config(self):
		module_logger.debug(_("Validating existing configurations."))
		pass
