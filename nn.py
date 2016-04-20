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
		d = Dataset(self._logger)
		self._logger.info("Loading dataset...")
		d.load_csvs_from_folder(CSV_DIR)
		self._logger.info("Done oading dataset")
		# TODO

	def build_model(self):
		self._logger.info("Building model...")
		self.model = Seq2seq(
			batch_input_shape=(TRAIN_BATCH_SIZE, INPUT_SEQ_LEN, 29),
			hidden_dim=HIDDEN_LAYER_DIM, 
			output_length=MAX_OUTPUT_TOKEN_LENGTH, 
			output_dim=29, # not sure if this is right
			depth=3,
			peek=True
		)
		self._logger.info("Compiling...")
		self.model.compile(loss='mse', optimizer='rmsprop')