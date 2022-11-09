from bs4 import BeautifulSoup
import requests
import logging
import sys
import spacy

nlp = spacy.load("en_core_web_sm")


def ner_analysis(tweet):
    '''
    ner_analysis function is used to extract the entities from the tweet.
    input : tweet
    output : list of entities
    '''
    logging.debug(f"Extracting the entities from the tweet, {tweet}")
    doc = nlp(tweet)
    logging.debug(f"Entities extracted from the tweet")
    return doc.ents


def check_actor(actor_name):
    '''
    check_actor function is used to check if the actor exists in the imdb database.
    input : actor_name
    output : True if the actor exists in the imdb database else False
    '''
    logging.info(f"Checking if the actor exists in the imdb database, {actor_name}")
    actor_name = actor_name.lower().strip()
    search_name = actor_name.replace(" ", "+")
    result = requests.get(
        f"https://www.imdb.com/search/name/?name={search_name}")
    if result.status_code == 200:
        soup = BeautifulSoup(result.text)
        all_models = soup.find_all("div", {"class": "lister-item mode-detail"})
        if len(all_models) > 0:
            for single_model in all_models:
                name = single_model.find_all("a")[1].text.lower().strip()
                role_type = single_model.find_all("p")
                if len(role_type) > 0:
                    role_type = role_type[0].text.split("|")[0].lower().strip()
                if name == actor_name and role_type in ["actor", "actress", "director"]:
                    logging.debug(
                        f"{role_type} exists in the imdb database, {actor_name}")
                    return True
        logging.debug(
            f"Role does not exists in the imdb database, {actor_name}")
        return False
    else:
        logging.critical("Error in fetching the url, please check the url/ internet connection")
        # stop the programme
        exit(1)


def find_all_names_data(data_path):
    '''
    find_all_names_data function is used to find all the names from the data_path.
    input : data_path
    output : list of names
    '''
    logging.info(f"Finding all the names from the data_path, {data_path}")
    names = []
    with open(data_path, 'r') as data_file:
        for tweet in data_file:
            ner_matches = ner_analysis(tweet)
            for ner_match in ner_matches:
                if ner_match.label_ == 'PERSON':
                    match = ner_match.text
                    names.append(match)
    logging.debug(f"Names found from the data_path, {data_path}")
    return names

if __name__ == "__main__":
    # Read argument
    # check_actor(sys.argv[1])
    # ner_analysis(sys.argv[1])
    logging.basicConfig(level=logging.DEBUG)
    with open ('all_names.txt', 'r') as f:
        f.write([f'{name}\n' for name in find_all_names_data('clean_tweet_data.txt')])
