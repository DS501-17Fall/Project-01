import json
import operator
import os

import matplotlib.pyplot as plt
from prettytable import PrettyTable
from wordcloud import WordCloud, STOPWORDS
from lib.word_utils import word_filter


def load_json(path):
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    return whole_data


# Define a function to get top words
def get_top_words(path, max_num, unwanted_words):
    # A list of all the tweets collected.
    whole_data = load_json(path)
    # A list of words which appear in the tweets
    word_list = []
    for data in whole_data:
        if 'text' not in data:
            continue
        word_list += data['text'].split()
    # A dictionary of words frequency, key is word, value is frequency
    frequency_dict = {}
    for word in word_list:
        word = word_filter(word)
        if word in unwanted_words:
            continue
        if len(word) > 0:
            frequency_dict[word] = frequency_dict.get(word, 0) + 1
    # A list of tuples (word, frequency), sorted by the frequency
    sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))
    # Print top table
    count = 0
    table = PrettyTable(['Rank', 'Word', 'Times'])
    for item in sorted_list:
        table.add_row([str(count + 1), item[0], item[1]])
        count = count + 1
        if count == max_num:
            break
    print(table)
    # Generate word map
    wordcloud = WordCloud(background_color="white", stopwords=STOPWORDS, width=800, height=400)
    wordcloud.generate_from_frequencies(frequencies=frequency_dict)
    wordcloud.to_file(path + '.png')
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


get_top_words(path='p1-data', max_num=30, unwanted_words=['nintendo', 'switch'])
