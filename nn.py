from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
import seq2seq
from seq2seq.models import Seq2seq
from dataset import Dataset
import os
import numpy as np

from config import *


class LSTMNet():
	def __init__(self, logger, batch_size=64):
		self._logger = logger
		self._logger.info("LSTMNet initialized.")

	def load_dataset(self):
		d = Dataset(self._logger)
		self._logger.info("Loading dataset...")
		self.X, self.y = d.load_csvs_from_folder(CSV_DIR)
		self._logger.info("Done loading dataset")
		self._logger.debug(str(self.X.shape))
		self._logger.debug(str(self.y.shape))

	def build_model(self):
		self._logger.info("Building model...")
		self.model = Seq2seq(
			batch_input_shape=(TRAIN_BATCH_SIZE, (INPUT_SEQ_LEN+1)*MSG_HISTORY_LEN, 29),
			hidden_dim=HIDDEN_LAYER_DIM, 
			output_length=MAX_OUTPUT_TOKEN_LENGTH, 
			output_dim=29, # not sure if this is right
			depth=3,
			peek=True
		)
		self._logger.info("Compiling...")
		self.model.compile(loss='mse', optimizer='rmsprop')

	def train(self, iters=None):
		if not iters:
			iters = TRAIN_ITERS

		for i in range(1, iters + 1):
			self._logger.info("Iteration " + str(i))

			for X_train, y_train in self.get_batches():
				self._logger.debug(str(X_train.shape))
				self._logger.debug(str(y_train.shape))

				self.model.fit(X_train, y_train, batch_size=TRAIN_BATCH_SIZE, nb_epoch=1, show_accuracy=True, verbose=1)

				self.save_weights()
				self.log_preds()

	def save_weights(self):
		self.model.save_weights(WEIGHTS_PATH, overwrite=True)

	def load_weights(self, fpath=None):
		if not fpath:
			fpath = WEIGHTS_PATH

		if os.path.isfile(fpath):
			self.model.load_weights(fpath)
		else:
			self._logger.warn("Error loading weights, initializing random weights. ")

	def get_batches(self, n=None):
		if n is None:
			# n = TRAIN_BATCH_SIZE
			n = 32000
		
		for i in xrange(0, len(self.X), n):
			yield self.X[i:i+n], self.y[i:i+n]

	def log_preds(self, test_sentences=["hello", "how are you", "what is the meaning of life"]):
		d = Dataset(self._logger)

		for s in test_sentences:
			seed = np.zeros((TRAIN_BATCH_SIZE, (MAX_OUTPUT_TOKEN_LENGTH+1)*MSG_HISTORY_LEN, 29), dtype="bool")
			blahhh=d.sample({"Msg": s})
			for i in range(len(blahhh)):
				for j in range(len(blahhh[i])):
					seed[0][i][j]=blahhh[i][j]

			self._logger.info(self.predict_sentence(seed))

	def predict_sentence(self, input_seq):
		preds = self.model.predict(input_seq, verbose=0)[0]
		self._logger.info(str(preds))
		sentence = ""
		for pred in preds:
			sentence += self.decode_text(self.sample_pred(pred))

		return sentence

	def sample_pred(self, a, temperature=1.0):
		return np.argmax(a)
		a = np.log(a) / temperature
		a = np.exp(a) / np.sum(np.exp(a))

		return np.argmax(np.random.multinomial(1, a, 1))

	def decode_text(self, n):
		if n == 1:
			return " "
		if n == 2:
			return "2"
		return chr(n + ord('a') - 3)

	def generate(self, input_sentences):
		if len(input_sentences) != MSG_HISTORY_LEN:
			self._logger.error("Invalid amount of input sentences. Must be equal to " + str(MSG_HISTORY_LEN))
			return ""

		sentences = []

		for s in input_sentences:
			sentences.append({"Msg": s[:INPUT_SEQ_LEN - 1]})

		d = Dataset(self._logger)

		seed = np.zeros((TRAIN_BATCH_SIZE, (MAX_OUTPUT_TOKEN_LENGTH+1)*MSG_HISTORY_LEN, 29), dtype="bool")
		samples = d.converttosamples(sentences)

		v = np.concatenate([samples[j] for j in range(0, MSG_HISTORY_LEN)])

		for i in range(len(v)):
			for j in range(len(v[i])):
				seed[0][i][j] = v[i][j]

		self._logger.info("Generating with seed " + str(input_sentences))

		return self.predict_sentence(seed)

