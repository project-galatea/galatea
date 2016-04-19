from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

class LSTMNet():
	def __init__(self, logger, batch_size=64):
		self.L = logger
		self.L.v("LSTMNet initialized.")
	def build_model(self):
		model = Sequential()
		# TODO