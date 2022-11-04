# find highest frequecy name in the file
import nltk
import sys
import re

def find_highest_frequency_name(file_name):
    # word count dictionary
    word_count = {}
    ignore_retweets = True
    with open(file_name) as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.startswith('RT') or ignore_retweets:
                host_regex = r"([A-Z][a-z]* [A-Z][a-z]*) and ([A-Z][a-z]* [A-Z][a-z]*) ([H|h]ost)"
                host_match = re.match(host_regex, line)
                if host_match:
                    host_one = host_match.group(1)
                    host_two = host_match.group(2)
                    if host_one in word_count:
                        word_count[host_one] += 1
                    else:
                        word_count[host_one] = 1
                    if host_two in word_count:
                        word_count[host_two] += 1
                    else:
                        word_count[host_two] = 1
    hosts = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:2]
    return [host[0] for host in hosts]

    
if __name__ == '__main__':
    print(find_highest_frequency_name(sys.argv[1]))
    