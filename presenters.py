import re
import spacy
import json
from utils import check_actor, ner_analysis
import logging
import difflib
import multiprocessing

nlp = spacy.load('en_core_web_sm')


def calculate_ratio(award, cat, winner, tweet):

    award_count = 0
    cat_count = 0
    winner_count = 0
    regex = f'{winner}'
    if re.search(regex, tweet):
        return 1
    regex = f'{award}'
    if re.search(regex, tweet):
        award_count += 1
    regex = f'{cat}'
    if re.search(regex, tweet):
        cat_count += 1
    if len(cat) == 0:
        return 0
    if winner in tweet:
        return 1
    for word in award.split():
        if word in tweet:
            award_count += 1
    for word in cat.split():
        if word in tweet:
            cat_count += 1
    print(award_count/len(award), cat_count/len(cat))
    if award_count/len(award) > 0.5 or cat_count/len(cat) > 0.5:
        return 1
    return 0

    # cat_ratio = difflib.SequenceMatcher(tweet, cat).ratio()
    # winner_ratio = 1 if winner in tweet else 0
    # return (award_ratio+cat_ratio+winner_ratio)/3
    # # return ( + cat_count/(len(cat)) + winner_count)/3



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
            regex = f'([P|p]resen\w+|[A|a]nnounc\w+|[I|i]ntroduc\w+) .* ([B|b]est .)'
            # regex = f'([P|p]resen\w+|[A|a]nnounc\w+|[I|i]ntroduc\w+) .*award'
            if re.search(regex, tweet):
                diff_score = []
                winners = []
                for award in awards:
                    # remove stop words
                    # award_vector = ' '.join([word for word in f'{award["award"].lower()} {award["category"]}'.split() if word not in nlp.Defaults.stop_words])
                    # diff_score.append(
                    #     difflib.SequenceMatcher(tweet_vector, award_vector).ratio())
                    diff_score.append(calculate_ratio(award["award"].lower(), award["category"].lower(), award["winner"], tweet.lower()))
                    winners.append(award["winner"])
                print(diff_score)

                matches = []
                max_score = max(diff_score)
                award_index = diff_score.index(max_score)
                if max_score == 1:
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
