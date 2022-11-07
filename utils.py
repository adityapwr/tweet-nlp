from bs4 import BeautifulSoup
import requests
import logging

'''
check_actor function is used to check if the actor exists in the imdb database.
input : actor_name
output : True if the actor exists in the imdb database else False
'''

logging.basicConfig(level=logging.INFO) 

def check_actor(actor_name):
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
                if name == actor_name:
                    logging.info(
                        f"Actor exists in the imdb database, {actor_name}")
                    return True
        logging.info(
            f"Actor does not exists in the imdb database, {actor_name}")
        return False
    else:
        logging.critical("Error in fetching the url, please check the url/ internet connection")
        # stop the programme
        exit(1)

