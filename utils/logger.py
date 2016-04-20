import os
import datetime
import time
import inspect
from config import *

class Logger():
	def __init__(self, logfile=None, verbose=False):
		self.log_levels = {
			0: "INFO",
			1: "DEBUG",
			2: "WARN",
			3: "ERROR",
		}

		self.verbose = verbose

		if logfile:
			self.logfile = logfile
		else:
			self.logfile = os.path.join(DEFAULT_LOG_DIR, datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d_%H:%M') + ".log")

	def info(self, msg):
		self.log(0, msg)

	def debug(self, msg):
		self.log(1, msg)

	def warn(self, msg):
		self.log(2, msg)

	def error(self, msg):
		self.log(3, msg)

	def log(self, lvl, msg):
		with open(self.logfile, "a") as logfile:
			callfunc = inspect.getouterframes(inspect.currentframe(), 2)[1][3] # Get name of function that called this
			ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
			log = ts + " : " + self.log_levels[lvl] + " " + " --- " + str(inspect.currentframe().f_back.f_locals['self']) + " in " + callfunc + " : " + msg
			if self.verbose:
				print log
			logfile.write(log)
