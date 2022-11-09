import re
import spacy
import json
from utils import check_actor, ner_analysis
import logging
import difflib
import multiprocessing

nlp = spacy.load('en_core_web_sm')


def calculate_ratio(str1, str2):
    count = 0
    for word in str1.split():
        if word in str2:
            count += 1
    return count / len(str1)


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
        
    with open(data_path, 'r') as data_file:
        for tweet in data_file:
            regex = f'([P|p]resen\w+|[A|a]nnounc\w+|[I|i]ntroduc\w+) .*award'
            if re.search(regex, tweet):
                diff_score = []
                winners = []
                # tweet_vector = ' '.join([word for word in tweet.lower(
                # ).split() if word not in nlp.Defaults.stop_words])
                for award in awards:
                    # remove stop words
                    # award_vector = ' '.join([word for word in f'{award["award"].lower()} {award["category"]}'.split() if word not in nlp.Defaults.stop_words])
                    # diff_score.append(
                    #     difflib.SequenceMatcher(tweet_vector, award_vector).ratio())
                    diff_score.append(calculate_ratio(
                        f'{award["award"].lower()} {award["category"].lower()}', tweet.lower()))
                    winners.append(award["winner"])
                print(diff_score)

                matches = []
                max_score = max(diff_score)
                award_index = diff_score.index(max_score)
                ner_matches = ner_analysis(tweet)
                for ner_match in ner_matches:
                    if ner_match.label_ == 'PERSON':
                        match = ner_match.text.lower().strip()
                        if match in imdb_checks.keys():
                            if imdb_checks[match]:
                                matches.append(match)
                        else:
                            if check_actor(match):
                                matches.append(match.title())
                                imdb_checks[match] = True
                            else:
                                imdb_checks[match] = False
                            
                # Find the max diff_score and get the award and category

                # get presenters and add the presenters count from matches to presenters
                awards[award_index]["presenters"] = awards[award_index].get(
                    "presenters", {})
                for match in matches:
                    if match in awards[award_index]["presenters"] and match not in winners:
                        awards[award_index]["presenters"][match] += 1
                    else:
                        awards[award_index]["presenters"][match] = 1
    with open("imdb_checks.json", 'w') as imdb_file:
        json.dump(imdb_checks, imdb_file)   
    return awards


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('final_list.json', 'r') as f:
        data = json.load(f)
        print(json.dumps(find_presenters(
            'clean_tweet_data.txt', data["awards"]), indent=4))
