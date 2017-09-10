import json
import operator
import os


def word_filter(word):
    skipping_words = ['rt', 'the', 'to', 'of', 'is', 'and', 'a', 'for', 'at', 'that', 'you',
                      'on', 'in', 'i', 'be', 'more', 'this', 'are', 'with', 'his', 'over', 'but', 'it',
                      'by', 'up', 'from', 'about', 'the', 'if', 'what', 'just', 'or', 'and', 'amp', 'me', 'be', 'than',
                      'as']
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


# A list of all the tweets collected.
whole_data = []
path = './data'
for filename in os.listdir(path):
    with open(path + '/' + filename, mode='r') as f:
        whole_data += json.load(f)

# A list of words which appear in the tweets
word_list = []
for data in whole_data:
    if 'text' not in data:
        continue
    word_list += data['text'].split()

# A dictionary of words frequency, key is word, value is appearing times
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

# Print top 30
count = 0
for item in sorted_list:
    print('Top ' + '{:4}'.format(str(count + 1)) + '{:25}'.format(item[0]) + ' ' + str(item[1]) + ' times')
    count = count + 1
    if count == 50:
        break
