import json
import operator
import os


# Define a function to get top retweets
def get_top_retweets(path, max_num):
    # A list of all the tweets collected.
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    # id_text_dict to store twitter ID and twitter text, and frequency_dict to store twitter ID and frequency
    id_text_dict = {}
    frequency_dict = {}
    for twitter in whole_data:
        if 'retweeted_status' not in twitter:
            continue
        retweet_dict = twitter['retweeted_status']
        id_text_dict[retweet_dict['id']] = retweet_dict['text']
        if retweet_dict['id'] in frequency_dict:
            frequency_dict[retweet_dict['id']] = frequency_dict[retweet_dict['id']] + 1
        else:
            frequency_dict[retweet_dict['id']] = 1
    # A list of tuples (word, frequency), sorted by the frequency
    sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))
    # Print top retweets
    count = 0
    for item in sorted_list:
        print('Top ' + str(count + 1) + '\t' + str(item[1]) + ' times')
        print(id_text_dict[item[0]])
        print('Link: https://twitter.com/i/web/status/' + str(item[0]) + '\n')
        count += 1
        if count == max_num:
            break


get_top_retweets('p1-data', 10)
