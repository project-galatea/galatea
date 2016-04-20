from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
import seq2seq
from seq2seq.models import Seq2seq
from dataset import Dataset

from config import *


class LSTMNet():
	def __init__(self, logger, batch_size=64):
		self._logger = logger
		self._logger.info("LSTMNet initialized.")

	def load_dataset(self):
		d = Dataset()
		d.load_csvs_from_folder(CSV_DIR)
		# TODO

	def build_model(self):
		self._logger.info("Building model...")
		model = Seq2seq(
			hidden_dim=HIDDEN_LAYER_DIM, 
			output_length=MAX_OUTPUT_TOKEN_LENGTH, 
			output_dim=20, 
			depth=3,
			peek=True
		)