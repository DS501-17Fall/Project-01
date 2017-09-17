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
    plt.title(path + ' twitter sentiment pie', fontsize=20, color='darkblue')
    plt.savefig(path + '-pie.png')
    plt.show()


# delete all punctuation
def clean_word(tweet):
    sentence = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ /  \ /  \S +)", " ", tweet).split())
    return sentence


def get_tweet_sentiment(tweet):
    sentence = clean_word(tweet)
    analysis = TextBlob(sentence)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'


def translate(text, language):
    if language != 'en':
        try:
            text = TextBlob(text).translate(from_lang=language, to='en')
        except:
            pass
    return text


def analyze_data(path, max_num, unwanted_words, language='en'):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    attitude_count = {'positive': 0, 'negative': 0, 'neutral': 0}
    attitude_word_frequency = {'positive': {}, 'negative': {}, 'neutral': {}}
    # id_original_text_dict is a dictionary to store twitter ID and twitter text not translated
    id_original_text_dict = {}
    # id_translated_text_dict is a dictionary to store twitter ID and twitter text translated
    id_translated_text_dict = {}
    # retweet_count_dict is a dictionary to store twitter ID and retweet count
    retweet_count_dict = {}
    for tweet in whole_data:
        if 'text' not in tweet:
            continue
        text = str(translate(tweet['text'], language))
        attitude = get_tweet_sentiment(text)
        attitude_count[attitude] += 1
        for word in text.split():
            word = word_filter(word)
            if len(word) > 0:
                attitude_word_frequency[attitude][word] = attitude_word_frequency[attitude].get(word, 0) + 1
        if 'retweeted_status' in tweet:
            retweet_dict = tweet['retweeted_status']
            id_original_text_dict[retweet_dict['id']] = retweet_dict['text']
            id_translated_text_dict[retweet_dict['id']] = text
            retweet_count_dict[retweet_dict['id']] = retweet_count_dict.get(retweet_dict['id'], 0) + 1
    for key in attitude_word_frequency:
        sorted_list = reversed(sorted(attitude_word_frequency[key].items(), key=operator.itemgetter(1)))
        count = 0
        table = PrettyTable(['Rank', 'Word', 'Times'])
        for item in sorted_list:
            if item[0] in unwanted_words:
                continue
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
        print(id_original_text_dict[item[0]])
        if language != 'en':
            print('Translated by Google: ' + id_translated_text_dict[item[0]])
        print('Link: https://twitter.com/i/web/status/' + str(item[0]))
        print('-'.rjust(100, '-'))
        count += 1
        if count == max_num:
            break
    draw_pie_chart(path, [attitude_count['positive'], attitude_count['negative'], attitude_count['neutral']])


print('Switch Result in English:')
analyze_data(path='switch', max_num=10, unwanted_words=['nintendo', 'switch'], language='en')
print('PS4 Result in English:')
analyze_data(path='ps4', max_num=10, unwanted_words=['sony', 'ps4'], language='en')
print('Xbox Result in English:')
analyze_data(path='xbox', max_num=10, unwanted_words=['xbox', 'one', 'microsoft'], language='en')

print('Switch Result in Japanese:')
analyze_data(path='switch-ja', max_num=10, unwanted_words=['nintendo', 'switch'], language='ja')
print('PS4 Result in Japanese:')
analyze_data(path='ps4-ja', max_num=10, unwanted_words=['sony', 'ps4'], language='ja')
print('Xbox Result in Japanese:')
analyze_data(path='xbox-ja', max_num=10, unwanted_words=['xbox', 'one', 'microsoft'], language='ja')
