import json
import operator
import os
from prettytable import PrettyTable


def get_top_tags(path, max_num):
    # A list of all the tweets collected.
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    # A dictionary of tag frequency, key is tag, value is frequency
    frequency_dict = {}
    for twitter in whole_data:
        if 'entities' not in twitter:
            continue
        if 'hashtags' not in twitter['entities']:
            continue
        tags = twitter['entities']['hashtags']
        if len(tags) == 0:
            continue
        for tag in tags:
            if tag['text'] in frequency_dict:
                frequency_dict[tag['text']] = frequency_dict[tag['text']] + 1
            else:
                frequency_dict[tag['text']] = 1
    # A list of tuples (word, frequency), sorted by the frequency
    sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))
    # Print top tags
    count = 0
    table = PrettyTable(['Rank', 'Hashtag', 'Times'])
    for item in sorted_list:
        table.add_row([str(count + 1), item[0], item[1]])
        count = count + 1
        if count == max_num:
            break
    print(table)


get_top_tags('data', 10)
