# find highest frequecy name in the file
import nltk
import sys
import re
import json
import logging

def find_host(data_path):
    '''
    find_host function is used to find the host of the show.
    '''
    # word count dictionary
    logging.info("***************Starting host search*****************")
    host_count = {}
    with open(data_path) as tweets_file:
        logging.info("Loading the data from the file")
        tweets = tweets_file.read().splitlines()
        if tweets is None:
            logging.critical("Please provide tweet data for the host search")
            exit(1)
        for tweet in tweets:
            host_regex = r"([A-Z][a-z]* [A-Z][a-z]*) and ([A-Z][a-z]* [A-Z][a-z]*) ([H|h]ost)"
            host_match = re.match(host_regex, tweet)
            if host_match:
                host_one = host_match.group(1)
                host_two = host_match.group(2)
                if host_one in host_count:
                    host_count[host_one] += 1
                else:
                    host_count[host_one] = 1
                if host_two in host_count:
                    host_count[host_two] += 1
                else:
                    host_count[host_two] = 1
    hosts = sorted(host_count.items(), key=lambda x: x[1], reverse=True)[:2]
    logging.info("Hosts search completed")
    return [host[0] for host in hosts]
    
if __name__ == '__main__':
    with open('hosts.json', 'w') as f:
        hosts = find_host("clean_tweet_data.txt")
        print(hosts)
        json.dump(hosts, f)
        
    