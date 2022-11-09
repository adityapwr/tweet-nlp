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
    logging.info("Finding the presenters from the data")
    with open("imdb_checks.json", 'a+') as imdb_file:
        try:
            imdb_checks = json.load(imdb_file)
        except json.decoder.JSONDecodeError:
            imdb_checks = {}
    logging.debug("imdb_checks loaded")
    logging.debug("Reading data fromd data_path")
    with open(data_path, 'r') as data_file:
        for award in awards:
            logging.debug(f"Finding presenters for {award['award']}")
            winner = award['winner']
            presenters = {}
            regex = re.compile(
                r"- [0-9]+ - (.*) ([P|p]resen\w+|[A|a]nnounc\w+|[I|i]ntroduc\w+) .* {{0}}".format(winner))

            logging.debug(f"Regex: {regex}")
            for tweet in data_file:
                presenter_search = regex.search(tweet)
                # print(presenter_search)
                print(presenter_search)
                if presenter_search:
                    print(presenter_search.group(1))
                    presenter = presenter_search.group(1)
                    presenter_ner = ner_analysis(presenter)
                    for ent in presenter_ner:
                        logging.debug(f"NER: {ent.text} {ent.label_}")
                        if ent.label_ == 'PERSON':
                            if ent.text not in imdb_checks.keys():
                                logging.debug("Checking IMDB")
                                imdb_checks[ent.text] = check_actor(ent.text)
                            if imdb_checks[ent.text]:
                                presenters[ent.text] = presenters.get(ent.text, 0) + 1
            award['presenters'] = presenters
    
    with open("imdb_checks.json", 'w') as imdb_file:
        json.dump(imdb_checks, imdb_file, indent=4)
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        logging.info("Starting presenter debugger")
        print(json.dumps(find_presenters(
            'clean_tweet_data.txt', data["awards"]), indent=4))
