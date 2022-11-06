import re
import spacy
import json

### find winners in the event and check with imdb database if the actor exists.
nlp = spacy.load("en_core_web_sm")


with open("all_data.txt", "r") as f:
    with open("winner_2.txt", "w") as w:
        # winner_regex = r'(winner|winners|nomminies) for (Best.+?)(,|in a)(.*) (is|are) (.*)'
        # winner_regex_2 = r'(.+?)(,|in a)(.*) ?(at the #GoldenGlobes)? \*\*\*winners are'
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
                        #if ent.text not in winners:
                        winners[ent.text] = winners.get(ent.text, 0) + 1
                        data[award] = data.get(award, {})
                        if category:
                            data[award][category] = data[award].get(category, {})
                            data[award][category][ent.text] = data[award][category].get(ent.text, 0) + 1
                        else:
                            data[award][ent.text] = data[award].get(ent.text, 0) + 1
            winner_regex_2 = r'(Best.+?)(,|in a)(.*) (is|are) (.*)'
            winner = re.search(winner_regex_2, line)
            if winner:
                award = winner.group(1).strip()
                category = winner.group(3).strip()
                doc = nlp(winner.group(5))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        #if ent.text not in winners:
                        winners[ent.text] = winners.get(ent.text, 0) + 1
                        data[award] = data.get(award, {})
                        if category:
                            data[award][category] = data[award].get(
                                category, {})
                            data[award][category][ent.text] = data[award][category].get(
                                ent.text, 0) + 1
                        else:
                            data[award][ent.text] = data[award].get(
                                ent.text, 0) + 1
            winner_regex_3 = r'(winner|winners) (is|are) (.*)'
            winner = re.search(winner_regex_2, line)
            if winner:
                # award = winner.group(1).strip()
                # category = winner.group(3).strip()
                # doc = nlp(winner.group(5))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        # if ent.text not in winners:
                        winners[ent.text] = winners.get(ent.text, 0) + 1
                        # data[award] = data.get(award, {})
                        # if category:
                        #     data[award][category] = data[award].get(
                        #         category, {})
                        #     data[award][category][ent.text] = data[award][category].get(
                        #         ent.text, 0) + 1
                        # else:
                        #     data[award][ent.text] = data[award].get(
                        #         ent.text, 0) + 1
        json.dump(data, w, indent=4)

        print(json.dumps(winners, indent=4))
        # nominees_list = {}
        # with open("nominees.txt", "r") as n:
        #     with open("nominees_2.txt", "w") as n2:
        #         nominees = n.read()
        #         for line in nominees.splitlines():
        #             for winner in winners:
        #                 if winner in line:
        #                     nom = nlp(line)
        #                     for ent in nom.ents:
        #                         if ent.label_ == "PERSON":
        #                             nominees_list[winner] = nominees_list.get(
        #                                 winner, set(winner))
        #                             nominees_list[winner].add(ent.text)
        #                 break
        #     json.dump(nominees_list, n2, indent=4)

        
            

            
