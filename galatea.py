from utils.logger import Logger as L
from nn import LSTMNet

class Galatea():
	def __init__(self):
		self.L = L("test.log", 1)
		self.net = LSTMNet(self.L)

g = Galatea()