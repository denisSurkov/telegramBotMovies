import logging

class Loggable():
	def __init__(self):
		FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
		self.logger = logging.getLogger("loger")
		self.logger.setLevel(logging.DEBUG)


	def log_it(message):
		logger.debug(message)