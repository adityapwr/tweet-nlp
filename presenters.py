import re
import spacy
import json
from utils import check_actor, ner_analysis
import logging
import difflib

nlp = spacy.load('en_core_web_sm')


def find_presenters(data_path, awards):
    imdb_checks = []

    with open(data_path, 'r') as data_file:
        for tweet in data_file:
            regex = f'([P|p]resen\w+ (the|this) (award|trophy) (to|for) (.*) )'
            if re.search(regex, tweet):
                diff_score = []
                winners = []
                tweet_vector = ' '.join([word for word in tweet.lower(
                ).split() if word not in nlp.Defaults.stop_words])
                for award in awards:
                    # remove stop words
                    award_vector = ' '.join([word for word in f'{award["award"].lower()} {award["category"]}'.split() if word not in nlp.Defaults.stop_words])
                    diff_score.append(
                        difflib.SequenceMatcher(tweet_vector, award_vector).ratio())
                    winners.append(award["winner"])
                    print(f'{tweet_vector}\n{award_vector}')
                print(diff_score)
            
                matches = []
                max_score = max(diff_score)
                award_index = diff_score.index(max_score)
                if max_score > 0.5:
                    ner_matches = ner_analysis(tweet)
                    for ner_match in ner_matches:
                        if ner_match.label_ == 'PERSON':
                            match = ner_match.text
                            if match in imdb_checks:
                                matches.append(match)
                            elif check_actor(match):
                                matches.append(match)
                                imdb_checks.append(match)
                ### Find the max diff_score and get the award and category 
                
                # get presenters and add the presenters count from matches to presenters
                    presenters = awards[award_index].get("presenters", {})
                    for match in matches:
                        if match in presenters and match not in winners:
                            presenters[match] += 1
                        else:
                            presenters[match] = 1
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        print(json.dumps(find_presenters('clean_tweet_data.txt', data["awards"]), indent=4))
        
