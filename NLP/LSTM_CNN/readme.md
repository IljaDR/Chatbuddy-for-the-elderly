#### Model training and validation ####

1. Install the required packages in:
	- requirements.txt 	<- CPU
	- requirements.gpu.txt 	<- GPU

2. Train a model:
	- Open the "Train Emotion Recognition Model.ipynb" with jupyter notebook
	- Run all the cells

3. Validate the model:
	- Open the "Emotion Recognition Model Validation.ipynb" with jupyter notebook
	- Run all the cells

#### Model implementation ####

Everything that is needed to deploy the model is contained in the "goldfish" folder. At this point, all the
required packages should already be installed.

To predict a sequence, run emofromtweet.py through the command line.
It will ask an input. You can write a sentence, in enlgish, and the model will return a string containing
the prediction scores for each emotion.

#### Citation

The data set used throughout the NLP exercise is the Lukas Garbas data set
https://github.com/lukasgarbas/nlp-text-emotion