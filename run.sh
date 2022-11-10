#!/bin/bash

YEAR="2015"
source nlp-project-1/bin/activate
pip install -r requirements.txt
python3 main.py gg-${YEAR}.json gg-${YEAR}-answers.json clean_tweet_data_${YEAR}.txt
