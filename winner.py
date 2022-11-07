import re
import spacy
import json
import requests
from bs4 import BeautifulSoup

# find winners in the event and check with imdb database if the actor exists.
nlp = spacy.load("en_core_web_sm")


def check_actor(org_name):
    org_name = org_name.lower().strip()
    search_name = org_name.replace(" ", "+")
    result = requests.get(f"https://www.imdb.com/search/name/?name={search_name}")
    soup = BeautifulSoup(result.text)
    all_models = soup.find_all("div", {"class": "lister-item mode-detail"})
    if len(all_models) > 0:
        for single_model in all_models:
            name = single_model.find_all("a")[1].text.lower().strip()
            if name == org_name:
                return True
    return False

with open("all_data.txt", "r") as f:
    with open("winner_2.txt", "w") as w:
        data = {}
        winners = {}
        text = f.read()
        for line in text.splitlines():
            winner_regex = r'(winner|winners|nomminiee|nomminies) for (Best.+?)(,|in a)(.*) (is|are) (.*)'
            winner = re.search(winner_regex, line)
            if winner:
                award = winner.group(2).strip()
                category = winner.group(4).strip()
                doc = nlp(winner.group(6))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        win = ent.text
                        # if ent.text not in winners:
                        winners[win] = winners.get(win, 0) + 1
                        data[win] = data.get(win, {})
                        if category:
                            data[win][award] = data[win].get(award, {})
                            data[win][award][category] = data[win][award].get(
                                category, 0) + 1
                        else:
                            data[win][award] = data[win].get(award, 0) + 1
            winner_regex_2 = r'(Best.+?)(,|in a)(.*) (is|are) (.*)'
            winner = re.search(winner_regex_2, line)
            if winner:
                award = winner.group(1).strip()
                category = winner.group(3).strip()
                doc = nlp(winner.group(5))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        # if ent.text not in winners:
                        win = ent.text
                        # if ent.text not in winners:
                        winners[win] = winners.get(win, 0) + 1
                        data[win] = data.get(win, {})
                        if category:
                            data[win][award] = data[win].get(award, {})
                            data[win][award][category] = data[win][award].get(
                                category, 0) + 1
                        else:
                            data[win][award] = data[win].get(award, 0) + 1
            winner_regex_3 = r'([B|b]est.*)(,|in a)(.*) [G|g]oes to ([A-Za-z]* [A-Za-z]*)'
            winner = re.search(winner_regex_3, line)
            if winner:
                award = winner.group(1).strip()
                category = winner.group(3).strip()
                doc = nlp(winner.group(4))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        # if ent.text not in winners:
                        win = ent.text
                        # if ent.text not in winners:
                        winners[win] = winners.get(win, 0) + 1
                        data[win] = data.get(win, {})
                        if category:
                            data[win][award] = data[win].get(award, {})
                            data[win][award][category] = data[win][award].get(
                                category, 0) + 1
                        else:
                            data[win][award] = data[win].get(award, 0) + 1
        
        final_winners = {}
        winners = {key: val for key, val in winners.items() if val > 2}
        for k, v in winners.items():
            # check if person exists from imdb url
            print(f'Checking {k}')
            if check_actor(k):
                print(f'Found {k}')
                final_winners[k] = v
            else:
                print(f'{k} not found')
        final_awards = []
        for k, v in final_winners.items():
            max = 0
            award = ""
            category = ""
            for k1, v1 in data[k].items():
                if type(v1) is dict:
                    for k2, v2 in v1.items():
                        if v2 > max:
                            max = v2
                            award = k1
                            category = k2
                else:
                    if v1 > max:
                        max = v2
                        award = k1
            final_awards.append({
                "award": award,
                "category": category,
                "winner": k
            })

        json.dump(final_awards, w, indent=4)
        print(json.dumps(final_awards, indent=4))
