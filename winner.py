import re
import spacy
import json

### find winners in the event and check with imdb database if the actor exists.
nlp = spacy.load("en_core_web_sm")


with open("all_data.txt", "r") as f:
    with open("winner_2.txt", "w") as w:
        winner_regex = r'(winner|winners|nomminies) for (Best.+?)(,|in a)(.*) (is|are) (.*)'
        # winner_regex_2 = r'(.+?)(,|in a)(.*) ?(at the #GoldenGlobes)? \*\*\*winners are'


        # for line in f:
        #     winner = re.search(winner_regex, line)
        #     if winner:
            
        #         w.write(f'{winner.group(2)} - {winner.group(4)} - {winner.group(6)}\n')
        #         w.write("\n")
        data = {}
        text = f.read()
        for line in text.splitlines():
            winner_regex = r'(winner|winners|nomminies) for (Best.+?)(,|in a)(.*) (is|are) (.*)'
            winner = re.search(winner_regex, line)
            if winner:
                doc = nlp(winner.group(6))
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        data[winner.group(2)] = data.get(winner.group(2), {})
                        data[winner.group(2)][winner.group(4)] = data[winner.group(2)].get(
                            winner.group(4), {})
                        data[winner.group(2)][winner.group(4)][ent.text] = data[winner.group(2)][winner.group(4)].get(ent.text, 0) + 1

        json.dump(data, w, indent=4)
            
