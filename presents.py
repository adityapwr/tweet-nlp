import re
import spacy
import json
from utils import check_actor
import logging

nlp = spacy.load('en_core_web_sm')


def find_presenter(award, category):
    regex = f'([P|p]resenter|[P|p]resenters|[P|p]resents).*({award}.*{category}|{award}|{category})'
    logging.info(f'Starting Regex search')
    logging.info(f'Current Search Regex: {regex}')
    presenters = {}
    matches = {}
    host = []
    logging.info("Loading hosts from hosts.json")
    with open('hosts.json') as f:
        host = json.load(f)
    logging.info("Loading data from all_data.txt")
    with open('all_data.txt', 'r') as f:
        for line in f:
            if re.search(regex, line):
                ent = nlp(line)
                for ent in ent.ents:
                    if ent.label_ == 'PERSON' and ent.text not in host:
                        presenter = ent.text.title()
                        logging.info(f'Found presenter: {presenter}')
                        if presenter in matches:
                            if matches[presenter]:
                                presenters[presenter] += 1
                        else:
                            if check_actor(presenter):
                                presenters[presenter] = 1
                                matches[presenter] = True
                            else:
                                matches[presenter] = False
    return presenters




if __name__ == '__main__':
    data = []
    with open('winner_2.json', 'r') as f:
        data = json.load(f)
        for award in data:
            presenters = find_presenter(award["award"], award["category"])
            award['presenters'] = presenters
        print(json.dumps(data, indent=4))
    
    with open('winner_2.json', 'w') as w:
        json.dump(data, w, indent=4)



