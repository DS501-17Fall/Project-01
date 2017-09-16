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
    for tweet in whole_data:
        if 'text' not in tweet:
            continue
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
        print(table, '\n')
    draw_pie_chart(path, [attitude_count['positive'], attitude_count['negative'], attitude_count['neutral']])


analyze_data(path='p4-data', max_num=10, language='en')
