import re
import json
from utils import check_actor, ner_analysis
import logging


def find_presenters(data_path, awards):
    '''
    find_presenters function is used to find the presenters from the data_path.
    input : data_path
    output : list of presenters
    '''
    logging.info("Finding the presenters from the data_path")

    logging.debug("Reading data fromd data_path")
    with open(data_path, 'r') as data_file:
        tweets = data_file.read()
        for award in awards:
            logging.debug(
                f"Finding presenters for {award['award']} {award['category']} {award['winner']}")
            winner = award['winner']
            presenters = {}
            for tweet in tweets.splitlines():
                presenter_search = re.search(
                    fr'- [0-9]+ - (.*) ([P|p]resen.+ |[A|a]nnounc.+ |[I|i]ntroduc.+ ).* {winner}', tweet)
                if presenter_search:
                    logging.debug(
                        f"Presenter search: {presenter_search.group(1)}")
                    presenter = presenter_search.group(1)
                    presenter_ner = ner_analysis(presenter)
                    for ent in presenter_ner:
                        if ent.label_ == 'PERSON':
                            if check_actor(ent.text.lower()):
                                logging.debug("Presenter found")
                                logging.debug("Adding presenter count")
                                presenters[ent.text] = presenters.get(ent.text, 0) + 1
            award['presenters'] = presenters
    logging.info("*********Completed finding presenters*********")
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        logging.info("Starting presenter debugger")
        print(json.dumps(find_presenters(
            'clean_tweet_data.txt', data["awards"]), indent=4))
