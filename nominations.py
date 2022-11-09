import re
import json
from utils import check_actor, ner_analysis
import logging


def find_nominations(data_path, awards):
    '''
    find_nominations function is used to find the nominations from the data_path.
    input : data_path
    output : list of nominations
    '''
    logging.info("Finding the nominations from the data")

    logging.debug("Reading data fromd data_path")
    with open(data_path, 'r') as data_file:
        for award in awards:
            logging.debug(f"Finding nominations for {award['award']}")
            nominations = {}
            for tweet in data_file:
                presenter_search = re.search(rf"- [0-9]+ - (.*) ([N|n]omin\w+) for {award['award']}.*{award['category']}", tweet)
                # print(presenter_search)
                print(presenter_search)
                if presenter_search:
                    print(presenter_search.group(1))
                    presenter = presenter_search.group(1)
                    presenter_ner = ner_analysis(presenter)
                    for ent in presenter_ner:
                        if ent.label_ == 'PERSON':
                            if check_actor(ent.text.lower()):
                                nominations[ent.text] = nominations.get(ent.text, 0) + 1
            award['nominations'] = nominations
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        logging.info("Starting presenter debugger")
        print(json.dumps(find_nominations(
            'clean_tweet_data.txt', data["awards"]), indent=4))
