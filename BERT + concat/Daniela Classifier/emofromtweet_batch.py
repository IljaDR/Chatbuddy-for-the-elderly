import pandas
from pandas import Series
from pathlib import Path
import pickle
from tensorflow.keras.models import load_model
from nlpp.utils import preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report

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

# Load the dataset into a pandas dataframe.
df = pandas.read_csv("data_full_clean_.csv", delimiter = ";", quoting=3, error_bad_lines=False) 
# Report the number of sentences.
print('Number of training sentences: {:,}\n'.format(df.shape[0]))

# Display 10 random rows from the data.
print(df)

class2idx_Daniela = {
    'anger':0,
    'fear':1,
    'joy':2,
    'neutral':3,
    'sadness':4,
}

df["Emotion"].replace(class2idx_Daniela, inplace=True)

print(df)

print(len(df.index))

train_limit = 7932
logits = []
labels = []
my_data = pandas.DataFrame(columns=['D_anger','D_fear','D_joy','D_neutral','D_sadness'])

for seq in range(len(df.index)):
    print(f'Processing: {seq}')
    
    sequence = Series(df["Text"][seq])
    sequence = preprocess(sequence)
    list_tokenized = tokenizer.texts_to_sequences(sequence)
    sequence = pad_sequences(list_tokenized, maxlen=100)
    predictions = model.predict(sequence)
    print(type(predictions))
    predictions_df = pandas.DataFrame({'D_anger':[predictions.item(0)],'D_fear':[predictions.item(1)],'D_joy':[predictions.item(2)],'D_neutral':[predictions.item(3)],'D_sadness':[predictions.item(4)]})
    my_data = my_data.append(predictions_df, ignore_index=True)

    pred = predictions.argmax(axis=1)
    if seq > train_limit:
        labels.extend([df["Emotion"][seq]])
        logits.extend([pred[0]])

print(my_data)
my_data.to_csv('daniela_output_all.csv', index=False)
print(classification_report(labels, logits))

'''
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
'''