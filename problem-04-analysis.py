import json
import operator
import os
import re

import matplotlib.pyplot as plt
from prettytable import PrettyTable
from textblob import TextBlob

from lib.word_utils import word_filter


def load_json(path):
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    return whole_data


def draw_pie_chart(path, data):
    labels = ['positive', 'neutral', 'negative']
    colors = ['yellowgreen', 'gold', 'coral']
    patches, texts, autotexts = plt.pie(data, colors=colors, labels=labels, autopct='%1.1f%%', shadow=True,
                                        startangle=90)
    for text in texts:
        text.set_fontsize(15)
    for autotext in autotexts:
        autotext.set_fontsize(15)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(path + '-pie.png')
    plt.show()


'''
The followings are three way to clean a tweet. The sentiment results differ on different topic. 
'''


# delete all punctuation, urls, and meaningless words
def clean_word_1(tweet):
    sentence = ''
    for word in tweet.split():
        word = word_filter(word)
        if len(word) > 0:
            sentence = sentence + ' ' + word
    return sentence


# delete all punctuation and urls, but preserve meaningless words
def clean_word_2(tweet):
    sentence = ''
    for word in tweet.split():
        word = word_filter(word, False)
        if len(word) > 0:
            sentence = sentence + ' ' + word
    return sentence


# delete all punctuation
def clean_word_3(tweet):
    sentence = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ /  \ /  \S +)", " ", tweet).split())
    return sentence


def get_tweet_sentiment(tweet):
    # sentence = clean_word_1(tweet)
    # sentence = clean_word_2(tweet)
    sentence = clean_word_3(tweet)
    analysis = TextBlob(sentence)
    # print('ORIGINAL:', tweet)
    # print('CLEANED:', sentence)
    # print(analysis.sentiment.polarity)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'


def analyze_data(path, max_num, language='en'):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    attitude_count = {'positive': 0, 'negative': 0, 'neutral': 0}
    attitude_word_frequency = {'positive': {}, 'negative': {}, 'neutral': {}}
    # id_text_dict is a dictionary to store twitter ID and twitter text
    id_text_dict = {}
    # retweet_count_dict is a dictionary to store twitter ID and retweet count
    retweet_count_dict = {}
    # favorite_count_dict is a dictionary to store twitter ID and favorite count
    favorite_count_dict = {}
    for tweet in whole_data:
        if 'retweet_count' in tweet and 'retweeted_status' in tweet:
            retweet = tweet['retweeted_status']
            id_text_dict[retweet['id']] = retweet['text']
            count = int(tweet['retweet_count'])
            if count > retweet_count_dict.get(retweet['id'], 0):
                retweet_count_dict[retweet['id']] = count
            count = int(tweet['retweeted_status']['favorite_count'])
            if count > favorite_count_dict.get(retweet['id'], 0):
                favorite_count_dict[retweet['id']] = count
        if 'text' in tweet:
            text = tweet['text']
            if language != 'en':
                try:
                    text = TextBlob(text).translate(from_lang=language, to='en')
                except:
                    pass
            attitude = get_tweet_sentiment(str(text))
            # print('Link to this tweet: https://twitter.com/i/web/status/' + str(tweet['id']) + '\n')
            attitude_count[attitude] += 1
            for word in tweet['text'].split():
                word = word_filter(word)
                if len(word) > 0:
                    attitude_word_frequency[attitude][word] = attitude_word_frequency[attitude].get(word, 0) + 1
    # Print top words
    for key in attitude_word_frequency:
        sorted_list = reversed(sorted(attitude_word_frequency[key].items(), key=operator.itemgetter(1)))
        count = 0
        table = PrettyTable(['Rank', 'Word', 'Times'])
        for item in sorted_list:
            table.add_row([str(count + 1), item[0], item[1]])
            count = count + 1
            if count == max_num:
                break
        print('Word count in', key, 'twitters:')
        print(table)
    # Print top retweet
    print('\n******Top Retweets******')
    sorted_list = reversed(sorted(retweet_count_dict.items(), key=operator.itemgetter(1)))
    count = 0
    for item in sorted_list:
        print('Top ' + str(count + 1) + '\t' + str(item[1]) + ' times')
        print(id_text_dict[item[0]])
        print('Link: https://twitter.com/i/web/status/' + str(item[0]))
        print('-'.rjust(100, '-'))
        count += 1
        if count == max_num:
            break
    # Print top favorite
    print('\n******Top Favorites******')
    sorted_list = reversed(sorted(favorite_count_dict.items(), key=operator.itemgetter(1)))
    count = 0
    for item in sorted_list:
        print('Top ' + str(count + 1) + '\t' + str(item[1]) + ' times')
        print(id_text_dict[item[0]])
        print('Link: https://twitter.com/i/web/status/' + str(item[0]))
        print('-'.rjust(100, '-'))
        count += 1
        if count == max_num:
            break
    draw_pie_chart(path, [attitude_count['positive'], attitude_count['negative'], attitude_count['neutral']])


analyze_data(path='p4-data', max_num=5, language='en')
