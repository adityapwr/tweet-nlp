'''
NLP Project 1
Tweet analysis is a tweet analyser based on the tweets of Golden Globes awards. 
Initially, the tweets are taken from the dataset and then the tweets are cleaned, 
transformed and stored in a different file. Then tweets are passed through the regex 
to find patterns and then the patterns are futher analysed. It uses the spacy library
to extract the entities from the tweets and then uses the IMDB API to find the actors 
and actresses from the tweets.
'''

# Importing the libraries
import json
import sys
import logging
from host import find_host
from winner import find_award_cat_win
from presenters import find_presenters
from nominations import find_nominations
from utils import setup


def transform_data(json_file_path, data_path):
    '''
    Transform_data function is used to transform the json data and store it in a different file as txt.
    '''
    logging.info("Transforming the data")
    with open(json_file_path, 'r') as json_file:
        logging.info("Loading the data from the file")
        json_data = json.load(json_file)

    if json_data is None:
        logging.critical("Please provide the data")
        exit(1)

    # Transforming the data
    with open(data_path, 'w') as f:
        logging.info("Transforming the data")
        for tweet in json_data:
            f.write(
                f'{tweet["timestamp_ms"]} - {tweet["user"]["id"]} - {tweet["text"]}\n')
    logging.info("Data transformed and stored in the file")


if __name__ == '__main__':
    setup()
    logging.info(
        "******************Starting the tweet analysis************************")
    logging.info("Loading the datapath from the command line argument")
    json_file_path = sys.argv[1]
    if json_file_path is None:
        logging.critical("Please provide the datapath")
        exit(1)
    logging.info(f"Data path is {json_file_path}")
    # read output path from the --output argument from command line
    output_json_path = sys.argv[2]
    logging.info(f"Output path is {output_json_path}")

    # Intermidiate data path
    data_path = sys.argv[3]
    logging.info(f"Data path is {data_path}")

    # Transforming the data
    transform_data(json_file_path, data_path)

    # Finding the hosts
    hosts = find_host(data_path)
    logging.info(f"Hosts found are {hosts}")

    # Finding the awards, categories and winners
    # actors = find_actors(data_path)
    awards = find_award_cat_win(data_path)

    # Finding the presenters
    awards_with_presenters = find_presenters(data_path, awards)

    # Finding the nominees
    awards_with_nominees = find_nominations(
        data_path, awards_with_presenters)

    with open(output_json_path, 'w') as f:
        json.dump({
            "hosts": hosts,
            "awards": awards,
        }, f)

    logging.info(
        "******************Ending the tweet analysis************************")
