# Keyword-based Vehicle Retrieval
This repository contains all files implemented for Keyword-based Vehicle Retrieval.

## Data Preparation
If you want to run or reproduce our code, you should download 2021 AI City Challenge Track 5 dataset.
We also used Track 3 dataset, but the data were preprocessed and included to the repository.

The two directories, train and validation, should be located in the current directory.

## Configuration Parameters
All the parameters for our best result are written in config.json.
You can edit and test it if you want.

## Pre-trained Model 
To train color and type of vehicles, we used a ResNet50 pre-trained on ImageNet dataset.

## Training
* To train from scratch, type this cmd in terminal: train.py -c config.json

## Testing
* To test from scratch, type this cmd in terminal: infer.py -c config.json

## How to reproduce the result
We used this checkpoint file to test.

[this checkpoint file]: https://drive.google.com/file/d/1pbfMF7n5Jgnz-jT2C6OFbCFAJFyumrCu/view?usp=sharing

We used [these files] for test acceleration.

[these files]: https://drive.google.com/file/d/1rPw-lKdJgaqtvUEcECXBMZl_UiWY3fpJ/view?usp=sharing

===============
Or leave it empty and use the [link text itself].

[link text itself]: http://www.reddit.com

===========

## GPU spec
TITAN Xp (Memory: 12GB)

