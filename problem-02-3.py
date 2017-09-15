import json
import operator
import os
from prettytable import PrettyTable


def load_json(path):
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    return whole_data


def get_top_tags(path, max_num):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    # A dictionary of tag frequency, key is tag, value is frequency
    frequency_dict = {}
    for twitter in whole_data:
        if 'entities' not in twitter or 'hashtags' not in twitter['entities']:
            continue
        tags = twitter['entities']['hashtags']
        if len(tags) == 0:
            continue
        for tag in tags:
            frequency_dict[tag['text']] = frequency_dict.get(tag['text'], 0) + 1
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


def get_top_mentions(path, max_num):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    # A dictionary of tag frequency, key is tag, value is frequency
    frequency_dict = {}
    id_name_dict = {}
    for twitter in whole_data:
        if 'entities' not in twitter or 'user_mentions' not in twitter['entities']:
            continue
        mentions = twitter['entities']['user_mentions']
        if len(mentions) == 0:
            continue
        for mention in mentions:
            frequency_dict[mention['id']] = frequency_dict.get(mention['id'], 0) + 1
            id_name_dict[mention['id']] = mention['screen_name']
    # A list of tuples (word, frequency), sorted by the frequency
    sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))
    # Print top tags
    count = 0
    table = PrettyTable(['Rank', 'ID', 'Screen-name', 'Times'])
    for item in sorted_list:
        table.add_row([str(count + 1), item[0], id_name_dict[item[0]], item[1]])
        count = count + 1
        if count == max_num:
            break
    print(table)


get_top_tags(path='p1-data', max_num=10)
get_top_mentions(path='p4-data', max_num=10)
