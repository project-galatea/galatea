import os
import datetime
import time
import inspect

class Logger():
	def __init__(self, logfile=None, mode=0):
		self.VERBOSE = 1
		self.NORMAL = 0

		if logfile:
			self.logfile = logfile
		else:
			self.logfile = os.path.join("logs/", datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d_%H:%M') + ".log")

		self.mode = mode

	def v(self, msg):
		with open(self.logfile, "a") as logfile:
			callfunc = inspect.getouterframes(inspect.currentframe(), 2)[1][3] # Get name of function that called this
			ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
			log = ts + " : VERBOSE " + " --- " + str(inspect.currentframe().f_back.f_locals['self']) + " in " + callfunc + " : " + msg
			if self.mode == self.VERBOSE:
				print log
			logfile.write(log)


