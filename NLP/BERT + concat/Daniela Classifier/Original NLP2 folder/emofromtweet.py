from pandas import Series
from pathlib import Path
import pickle
from tensorflow.keras.models import load_model
from nlpp.utils import preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences

def get_tokenizer_and_encoder(tokenizer_path, encoder_path):
    with tokenizer_path.open('rb') as file:
        tokenizer = pickle.load(file)

    with encoder_path.open('rb') as file:
        encoder = pickle.load(file)

    return tokenizer, encoder

tokenizer_path = Path('tokenizer.pickle').resolve()
encoder_path = Path('encoder.pickle').resolve()
tokenizer, encoder = get_tokenizer_and_encoder(tokenizer_path, encoder_path)

model = load_model('model.h5', compile=False)

sequence = Series([input('Type a sentence: ')])
sequence = preprocess(sequence)
list_tokenized = tokenizer.texts_to_sequences(sequence)
sequence = pad_sequences(list_tokenized, maxlen=100)
predictions = model.predict(sequence)
pred = predictions.argmax(axis=1)

result = f"""
outputs:    {predictions[0]}
classes:    {encoder.classes_}
argmax:     {pred[0]}
emotion:    {encoder.classes_[pred[0]]}
"""

print(result)