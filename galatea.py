from utils.logger import Logger as L
from nn import LSTMNet

class Galatea():
	def __init__(self):
		self._logger = L("test.log", 1)
		self.net = LSTMNet(self._logger)
		self.net.load_dataset()
		self.net.build_model()
		self.net.train()

g = Galatea()