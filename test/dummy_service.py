#! /usr/bin/env python

import os
import sys
import time
import logging

base_dir = os.path.abspath(".")
sys.path.append(base_dir)

from system_v import service

pidfile   = os.path.join(base_dir, "dat/dummy.pid")
logfile   = os.path.join(base_dir, "dat/dummy.log")
data_file = os.path.join(base_dir, "dat/dummy.dat")

class dummy_service(service):
	def __init__(self):
		super(dummy_service, self).__init__("dummy_service", pidfile, logfile)
		self.terminating = False

	def run(self):
		logging.basicConfig(stream=self.log, level=logging.DEBUG)

		try:
			self.fd = open(data_file, "w+")
		except Exception as e:
			logging.critical("Open failed: {0}".format(e))
			self.log_status(False)
			sys.exit(1)
		else:
			self.log_status(True)

		while True:
			try:
				self.fd.write("Poop\n")
				self.fd.flush()
			except Exception as e:
				logging.warning("Write failed: {0}".format(e))
			time.sleep(1)

	def terminate(self, signal, frame):
		if not self.terminating:
			self.terminating = True
			self.fd.write("Terminated\n")
			self.fd.close()
			self.log.close()
			sys.exit(0)

s = dummy_service()
r = {
	"start"        : s.start,
	"stop"         : s.stop,
	"restart"      : s.restart,
	"try-restart"  : s.try_restart,
	"reload"       : s.reload,
	"force-reload" : s.force_reload,
	"status"       : s.status
}.get(sys.argv[1], s.usage)()
sys.exit(r)
