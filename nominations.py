import json
import re


def find_nominiees(award, category):
    with open("all_data.txt", "r") as f:
        # search for nominees in the text
        text = f.read()
        # create a regex filter for nominees
        #regex = f'([N|n]ominee|[N|n]ominees) for {award}.*{category} (is|are) (.*)'
        regex = f'([N|n]omin[a-z]\w+) for {award}.*{category} (is|are) (.*)'
        matches =[]
        for line in text.splitlines():
            match = re.search(regex, line)
            if match:
                matches = matches.extend(match.group(3).split(","))
        return matches


with open("nominations.txt", "w") as w:
    ### read winner_2.json and find nominees for each award category
    with open("winner_2.json", "r") as f2:
        data = json.load(f2)
        nominiees = []
        for award in data:
            award_nominees = find_nominiees(award["award"], award["category"])
            nominiees.append({
                "award": award["award"],
                "category": award["category"],
                "nominees": award_nominees
            })
    print(nominiees)
    json.dump(nominiees, w, indent=4)
