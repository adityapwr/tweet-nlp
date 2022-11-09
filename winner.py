import re
import logging
from utils import check_actor, ner_analysis


def extract_data(winner_ner, winners_list, winner_map, award, category):
    '''
    Extract data from winner_ner and add to winners_list and winner_map
    '''
    for ent in winner_ner:
        if ent.label_ == "PERSON":
            # if ent.text not in winners_list:
            win = ent.text
                # if ent.text not in winners_list:
            winners_list[win] = winners_list.get(win, 0) + 1
            winner_map[win] = winner_map.get(win, {})
            if category:
                winner_map[win][award] = winner_map[win].get(
                    award, {})
                winner_map[win][award][category] = winner_map[win][award].get(
                    category, 0) + 1
            else:
                winner_map[win][award] = winner_map[win].get(
                    award, 0) + 1
    
def validate_winners(winners_list):
    '''
    validate_winners function is used to validate the winner list against IMDB
    input : winners_list
    output : list of validated winners
    '''
    logging.info("Validating winners against IMDB")
    final_winners_list = {}
    for key, val in winners_list.items():
        if check_actor(key):
            final_winners_list[key] = val
    return final_winners_list


def transform_data(final_winners_list, winner_map):
    '''
    transform_data function is used to transform the data into a list of dictionaries
    input : award_list
    output : list of dictionaries
    '''
    logging.info("Transforming data into a list of dictionaries")
    award_list = []
    for actor in final_winners_list:
        max_count = 0
        final_award = ""
        final_category = ""
        for award, categories in winner_map[actor].items():
            if type(categories) is dict:
                for category, count in categories.items():
                    if count > max_count:
                        max_count = count
                        final_award = award
                        final_category = category
            else:
                if count > max_count:
                    max_count = count
                    final_award = award
        award_list.append({
            "award": final_award,
            "category": final_category,
            "winner": actor
        })
    logging.debug("Data transformation completed")
    return award_list

def find_award_cat_win(data_path):
    '''
    find_award_cat_win function is used to find the award, category and winner from the data_path.
    input : data_path
    output : list of award, category and winner
    '''
    logging.info("Starting award, category, winner search")
    with open(data_path, "r") as f:
        winner_map = {}
        winners_list = {}
        logging.info("Loading tweets from data_path")
        tweets = f.read()
        for tweet in tweets.splitlines():
            regex = r'(winner|winners) for (Best.+?)(,|in a)(.*) (is|are) (.*)'
            logging.debug(f"Trying first regex search {regex}")
            search_result = re.search(regex, tweet)
            if search_result:
                award = search_result.group(2).strip()
                category = search_result.group(4).strip()
                winner_ner = ner_analysis(search_result.group(6))
                extract_data(winner_ner, winners_list,
                             winner_map, award, category)
            logging.debug(f"First regex search completed")
            
            regex = r'(Best.+?)(,|in a)(.*) (is|are) (.*)'
            logging.debug(f"Trying second regex search, {regex}")
            search_result = re.search(regex, tweet)
            if search_result:
                award = search_result.group(1).strip()
                category = search_result.group(3).strip()
                winner_ner = ner_analysis(search_result.group(5))
                extract_data(winner_ner, winners_list,
                             winner_map, award, category)
            logging.debug(f"Second regex search completed")

            regex = r'([B|b]est.*)(,|in a)(.*) [G|g]oes to ([A-Za-z]* [A-Za-z]*)'
            logging.debug(f"Trying third regex search, {regex}")
            search_result = re.search(regex, tweet)
            if search_result:
                award = search_result.group(1).strip()
                category = search_result.group(3).strip()
                winner_ner = ner_analysis(search_result.group(4))
                extract_data(winner_ner, winners_list, winner_map, award, category)
            logging.debug(f"Third regex search completed")
        
        
        # winners_list = {key: val for key, val in winners_list.items() if val > 2}
        final_winners_list = validate_winners(winners_list)
        award_list = transform_data(final_winners_list, winner_map)
        logging.info("Award, Category, Winner search completed")
        return award_list


if __name__ == "__main__":
    print(find_award_cat_win("winner.txt"))