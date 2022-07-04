
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Embedding, Dense, Bidirectional, Dropout
import pickle
with open("model.pkl", "rb") as f:
  lmodel = pickle.load(f)


# x = lmodel()
x = Sequential()
print('done')
# print(lmodel.summary())
