# pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
# pip3 install transformers
# pip3 install pandas

import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
from keras_preprocessing.sequence import pad_sequences
from datetime import datetime
from sklearn.metrics import classification_report

# We will run on the CPU
device = torch.device("cpu")

# Load previously saved tokenizer
tokenizer_path = './output_trained_model'
tokenizer = BertTokenizer.from_pretrained(tokenizer_path, do_lower_case=True)

# Load previously saved model
model_path = './output_trained_model'
model = BertForSequenceClassification.from_pretrained(model_path)

def validate_emo(model, tokenizer, utterances, max_lenght=0):

    # Tokenize the utterances
    input_ids = []
    for utt in utterances:
        encoded_sent = tokenizer.encode(
                            utt,                        # utterances to encode
                            add_special_tokens = True,  # Add '[CLS]' and '[SEP]'
                    )
        input_ids.append(encoded_sent)

    # pad the encoded input_ids
    if max_lenght == 0:
        max_lenght = len(encoded_sent)

    input_ids = pad_sequences(input_ids, maxlen=max_lenght, dtype="long", 
                          value=0, truncating="post", padding="post")

    # Create attention masks
    attention_masks = []
    # For each utterance...
    for sent in input_ids:
        
    # Create the attention mask.
        #   - If token ID is 0, then it is padding => set mask to 0
        #   - If token ID is > 0, then it is a real token => set mask to 1
        att_mask = [float(token_id > 0) for token_id in sent]
        
        # Store attention mask for utterance
        attention_masks.append(att_mask)                      

    # Convert all inputs into torch tensors
    validation_inputs = torch.tensor(input_ids)
    validation_masks = torch.tensor(attention_masks)

    model.eval()

    with torch.no_grad():
        outputs = model(validation_inputs, 
                        token_type_ids=None, 
                        attention_mask=validation_masks)   
    logits = outputs[0]
    logits_flat = np.argmax(logits, axis=1).flatten()
    emotion = logits_flat[0].item()

    return logits
'''
def validate_emo(model, tokenizer, utterances, max_lenght=0):

    logits = validate_sentence(model, tokenizer, utterances, max_lenght)
    logits_flat = np.argmax(logits, axis=1).flatten()
    emotion = logits_flat[0].item()

    return emotion
'''
def emotion_int_to_str(emo_int):
    if emo_int == 0:
        return 'sadness'
    elif emo_int == 1:
        return 'neutral'
    elif emo_int == 2:
        return 'anger'
    elif emo_int == 3:
        return 'fear'
    elif emo_int == 4:
        return 'joy'
    else:
        return 'unknown'


# Load the dataset into a pandas dataframe.
df = pd.read_csv("data_full_clean_.csv", delimiter = ";", quoting=3, error_bad_lines=False) 
# Report the number of sentences.
print('Number of training sentences: {:,}\n'.format(df.shape[0]))

# Display 10 random rows from the data.
print(df)

class2idx_Alexa = {
    'sadness':0,
    'neutral':1,
    'anger':2,
    'fear':3,
    'joy':4,
}

df["Emotion"].replace(class2idx_Alexa, inplace=True)

print(df)

print(len(df.index))

train_limit = 7932
logits = []
labels = []
max_lenght = 100
my_data = pd.DataFrame(columns=['A_sadness','A_neutral','A_anger','A_fear','A_joy'])

for seq in range(len(df.index)):

    print(f'Processing: {seq}')
    sentence = df["Text"][seq]
    my_logits = validate_emo(model=model, tokenizer=tokenizer,utterances=[sentence],max_lenght=100)
    #print(f"{my_logits[0][0].item()},{my_logits[0][1].item()},{my_logits[0][2].item()},{my_logits[0][3].item()},{my_logits[0][4].item()}")
    
    predictions_df = pd.DataFrame({'A_sadness':[my_logits[0][0].item()],'A_neutral':[my_logits[0][1].item()],'A_anger':[my_logits[0][2].item()],'A_fear':[my_logits[0][3].item()],'A_joy':[my_logits[0][4].item()]})
    my_data = my_data.append(predictions_df, ignore_index=True)

    my_logits_flat = np.argmax(my_logits, axis=1).flatten()
    my_emotion = my_logits_flat[0].item()

    if seq > train_limit:
        labels.extend([df["Emotion"][seq]])
        logits.extend([my_emotion])


    #now = datetime.now()
    #print(now)
    #print(emotion_int_to_str(my_emotion))
    #print(my_emotion)

print(my_data)
my_data.to_csv('alexa_output_all.csv', index=False)
print(classification_report(labels, logits))







'''
sentence = input("Type a sentence: ")

emotion = validate_emo(model=model, tokenizer=tokenizer,utterances=[sentence],max_lenght=100)
now = datetime.now()
print(now)
print(emotion_int_to_str(emotion))
print(emotion)
'''