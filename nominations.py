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
                nomination_search = re.search(
                    rf"- [0-9]+ - (.*) ([N|n]omin\w+) for {award['award']}.*{award['category']}", tweet, re.IGNORECASE)
                if nomination_search:
                    nominiee = nomination_search.group(1)
                    nominiee_ner = ner_analysis(nominiee)
                    for ent in nominiee_ner:
                        if ent.label_ == 'PERSON':
                            if check_actor(ent.text.lower()):
                                nominations[ent.text] = nominations.get(
                                    ent.text, 0) + 1
                nomination_search = re.search(
                    rf".*{award['award']}.*{award['category']}.*([N|n]omin\w+) (is|are) (.*)", tweet, re.IGNORECASE)
                if nomination_search:
                    nominiee = nomination_search.group(3)
                    nominiee_ner = ner_analysis(nominiee)
                    for ent in nominiee_ner:
                        if ent.label_ == 'PERSON':
                            if check_actor(ent.text.lower()):
                                nominations[ent.text] = nominations.get(
                                    ent.text, 0) + 1
                nomination_search = re.search(
                    rf"([N|n]omin\w+) for {award['award']}.*{award['category']}(.*)", tweet, re.IGNORECASE)
                if nomination_search:
                    nominiee = nomination_search.group(2)
                    nominiee_ner = ner_analysis(nominiee)
                    for ent in nominiee_ner:
                        if ent.label_ == 'PERSON':
                            if check_actor(ent.text.lower()):
                                nominations[ent.text] = nominations.get(
                                    ent.text, 0) + 1
            award['nominations'] = nominations
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        logging.info("Starting nominiee debugger")
        print(json.dumps(find_nominations(
            'clean_tweet_data.txt', data["awards"]), indent=4))
