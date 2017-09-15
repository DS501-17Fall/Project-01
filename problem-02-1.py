import json
import operator
import os


def load_json(path):
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    return whole_data


# Define a function to get top retweets
def get_top_retweets(path, max_num):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    # id_text_dict is a dictionary to store twitter ID and twitter text
    id_text_dict = {}
    # frequency_dict is a dictionary to store twitter ID and frequency
    frequency_dict = {}
    for twitter in whole_data:
        if 'retweeted_status' not in twitter:
            continue
        retweet_dict = twitter['retweeted_status']
        id_text_dict[retweet_dict['id']] = retweet_dict['text']
        frequency_dict[retweet_dict['id']] = frequency_dict.get(retweet_dict['id'], 0) + 1
    # A list of tuples (word, frequency), sorted by the frequency
    sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))
    # Print top retweets
    count = 0
    for item in sorted_list:
        print('Top ' + str(count + 1) + '\t' + str(item[1]) + ' times')
        print(id_text_dict[item[0]])
        print('\nLink to this tweet: https://twitter.com/i/web/status/' + str(item[0]))
        print('-'.rjust(100, '-'))
        count += 1
        if count == max_num:
            break


get_top_retweets(path='p1-data', max_num=10)
