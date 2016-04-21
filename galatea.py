from utils.logger import Logger as L
from nn import LSTMNet

class Galatea():
	def __init__(self):
		self._logger = L("test.log", 1)
		self.net = LSTMNet(self._logger)
		self.net.load_dataset()
		self.net.build_model()
		self.net.load_weights()

	def train(self):
		self.net.train()

	def generate(self, input_sentences):
		return self.net.generate(input_sentences)		


def main():
	g = Galatea()

	g.generate(["hello", "how are you"])

if __name__ == '__main__':
	main()