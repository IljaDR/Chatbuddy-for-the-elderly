# Chatbuddy for the elderly

This is a group project that was made for the Intelligent Interfaces assignment as part of the Applied AI postgraduate at Erasmushogeschool Brussels.
The goal of this project is to give the elderly companionship while enabling the monitoring of their mood over time.

## Project overview

You can see the general overview of the goldfish part of the project below:

![Overview](https://i.imgur.com/YWpg86y.png)

The user will speak to a fish, their voice will get converted to text, the fish will respond visually to what the user has said. In parallel to this, a BERT and LSTM model will process the text and output a more accurate emotion, which will get added to a report for the caregiver.

An overview of the web app can be found in the web app directory.

## Demos

Goldfish: https://youtu.be/WKuefSmIiRE
Web app: https://youtu.be/nGJsVy-3r4k

## Instructions

This project consists of a couple of different parts. To run everything, you need to start by generating a BERT and LSTM CNN model. Instructions on how to do so can be found in the BERT + concat and NLP_LSTM_CNN directory respectively. Once that is done, you can follow the instructions in the integration directory to make the Goldfish work. To use the web app, follow instructions in web app directory.

## Original repos

The goal of this repository is to bundle the code of all group members together, below you can find the original repos that were used by those who used version control to write their code:

Web app: https://github.com/ReggieVW/ChatBuddy

Integration: https://github.com/IljaDR/Fish-emotion-engine

Unity interface: https://github.com/IljaDR/Chatbuddy
