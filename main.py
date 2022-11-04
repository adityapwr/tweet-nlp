# import the json dataset and initialize the script frame NLP project 1

import json
import sys
import re

# import the json dataset
if __name__ == '__main__':
    # read data path from the --data argument from command line
    data_path = sys.argv[1]
    
    with open(data_path, 'r') as f:
        data = json.load(f)

# 1. Host(s) (for the entire ceremony)
# 2. Award Names
# 3. Award categories
# Presenters
# 4. Nominees, Favorites, Winners mapped to awards*
# 5. Winners, mapped to awards*

    with open('all_data.txt', 'a') as f:
        for tweet in data:
            f.write(tweet['text'])
            f.write('\n')
        # print all tweets in one file


    # for tweet in data:
    #     # segreate tweets in multiple files based on the type of tweet, if it has host place it in host file. If it has winner place it in winner file
    #     # create a regex filter for host
    #     host = re.compile(r'host')
    #     # create a regex filter for award name
    #     award = re.compile(r'award')
    #     # create a regex filter for winner
    #     winner = re.compile(r'winner')
    #     # create a regex filter for categories
    #     categories = re.compile(r'category')
    #     # create a regex filter for nominees
    #     nominees = re.compile(r'nominees')
    #     # create a regex filter for presenters
    #     presenter = re.compile(r'presenter')
    #     # create a regex filter for performers
    #     performer = re.compile(r'performer')
    #     # create a regex filter for favorites
    #     favorites = re.compile(r'favorites')

    #     # check if the tweet has host
    #     if host.search(tweet['text']):
    #         # write the tweet to host file
    #         with open('host.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has winner
    #     elif winner.search(tweet['text']):
    #         # write the tweet to winner file
    #         with open('winner.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has categories
    #     elif categories.search(tweet['text']):
    #         # write the tweet to categories file
    #         with open('categories.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has nominees 
    #     elif nominees.search(tweet['text']):
    #         # write the tweet to nominees file
    #         with open('nominees.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has presenters
    #     elif presenter.search(tweet['text']):
    #         # write the tweet to presenters file
    #         with open('presenters.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has performers
    #     elif performer.search(tweet['text']):
    #         # write the tweet to performers file
    #         with open('performers.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has favorites
    #     elif favorites.search(tweet['text']):
    #         # write the tweet to favorites file
    #         with open('favorites.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # check if the tweet has award
    #     elif award.search(tweet['text']):
    #         # write the tweet to award file
    #         with open('award.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
    #     # if the tweet does not have any of the above keywords
    #     else:
    #         # write the tweet to other file
    #         with open('other.txt', 'a') as f:
    #             f.write(tweet['text'])
    #             f.write('\n')
            

    


