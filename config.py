# GALATEA CONFIG
# ~~~~~~~~~~~~~~~

# Logger config

DEFAULT_LOG_DIR = 'logs/'

# ---------------------------------------


# seq2seq config

INPUT_SEQ_LEN = 10
MAX_OUTPUT_TOKEN_LENGTH = 11
HIDDEN_LAYER_DIM = 64
MSG_HISTORY_LEN = 2

# ---------------------------------------

# Dataset config

CSV_DIR = "data"
SAVE_X = "dataset_X.npy"
SAVE_Y = "dataset_y.npy"

# ---------------------------------------

# Training config

TRAIN_BATCH_SIZE = 64
TRAIN_ITERS = 100
WEIGHTS_PATH = "model_weights.h5"
SAVE_WEIGHT_FREQ = 100

# ---------------------------------------


# Generation config


# ---------------------------------------
