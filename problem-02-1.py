import json
import operator
import os
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def word_filter(word):
    skipping_words = ['rt', 'amp', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once',
                      'during', 'out', 'very',
                      'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
                      'of', 'most',
                      'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
                      'themselves',
                      'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
                      'her', 'more',
                      'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours',
                      'had',
                      'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in',
                      'will', 'on',
                      'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
                      'now',
                      'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which',
                      'those', 'i',
                      'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'a', 'by', 'doing', 'it', 'how',
                      'was', 'here', 'than', 'us']
    if word in skipping_words:
        return False
    elif ord(word[0]) > 255:
        return False
    elif word.startswith('@'):
        return False
    elif word.startswith('#'):
        return False
    elif word.startswith('http'):
        return False
    else:
        return True


def word_trim(word):
    start = 0
    end = len(word) - 1
    while start <= end:
        asc2 = ord(word[start])
        if 47 < asc2 < 58 or 63 < asc2 < 91 or 96 < asc2 < 123 or asc2 == 35:
            break
        else:
            start += 1
    while start <= end:
        asc2 = ord(word[end])
        if 47 < asc2 < 58 or 63 < asc2 < 91 or 96 < asc2 < 123 or asc2 == 35:
            break
        else:
            end -= 1
    if start > end:
        return ""
    else:
        return word[start:end + 1]


# Define a function to get top words
def get_top_words(path, max_num):
    # A list of all the tweets collected.
    whole_data = []
    path = './' + path
    for filename in os.listdir(path):
        with open(path + '/' + filename, mode='r') as f:
            whole_data += json.load(f)
    # A list of words which appear in the tweets
    word_list = []
    for data in whole_data:
        if 'text' not in data:
            continue
        word_list += data['text'].split()
    # A dictionary of words frequency, key is word, value is frequency
    frequency_dict = {}
    for word in word_list:
        word = word_trim(word)
        word = word.lower()
        if len(word) > 0 and word_filter(word):
            if word in frequency_dict:
                frequency_dict[word] = frequency_dict[word] + 1
            else:
                frequency_dict[word] = 1
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
    wordcloud.to_file('problem-02-1.png')
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


get_top_words('data', 30)
