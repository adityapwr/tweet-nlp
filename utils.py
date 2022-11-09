import pickle
from bs4 import BeautifulSoup
import requests
import logging
import spacy
import sys
nlp = spacy.load("en_core_web_sm")

IMDB_LOCAL_DB = 'imdb_file.pkl'


def setup():
    '''
    setup function is used to setup the imdb database.
    '''
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Setting up the imdb database")

    try:
        imdb_file = open(IMDB_LOCAL_DB, 'rb')
        inital_data = pickle.load(imdb_file)
        imdb_file.close()
    except EOFError:
        inital_data = {}
    logging.info(f"IMDB local data loaded: {inital_data}")
    imdb_file = open(IMDB_LOCAL_DB, 'wb')
    pickle.dump(inital_data, imdb_file, protocol=pickle.HIGHEST_PROTOCOL)
    imdb_file.close()
    logging.info("Imdb database setup completed")

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
    imdb_file = open(IMDB_LOCAL_DB, 'rb')
    imdb_checks = pickle.load(imdb_file)
    imdb_file.close()

    logging.info(
        f"Checking if the actor, {actor_name} exists in the imdb database")
    actor_name = actor_name.lower().strip()
    if actor_name in imdb_checks.keys():
        logging.debug("Actor exists in the local imdb database")
        return imdb_checks[actor_name]
    search_name = actor_name.replace(" ", "+")
    result = requests.get(
        f"https://www.imdb.com/search/name/?name={search_name}")
    if result.status_code == 200:
        soup = BeautifulSoup(result.text, features="html.parser")
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
                    imdb_checks[actor_name] = True
                    imdb_file = open(IMDB_LOCAL_DB, 'wb')
                    pickle.dump(
                        imdb_checks, imdb_file, protocol=pickle.HIGHEST_PROTOCOL)
                    imdb_file.close()
                    return True

        logging.debug(
            f"Role does not exists in the imdb database, {actor_name}")
        imdb_checks[actor_name] = False
        imdb_file = open(IMDB_LOCAL_DB, 'wb')
        pickle.dump(
            imdb_checks, imdb_file, protocol=pickle.HIGHEST_PROTOCOL)
        imdb_file.close()
        return False
    else:
        logging.error(f"Error in the request, {result.status_code}")
        # stop the programme if the request fails
        exit(1)


if __name__ == "__main__":
    # Read argument
    # check_actor(sys.argv[1])
    # ner_analysis(sys.argv[1])
    setup()
    logging.basicConfig(level=logging.DEBUG)
    check_actor(sys.argv[1])
