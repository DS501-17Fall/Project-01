import json
import operator

# A list of all the tweets collected.
whole_data = []
with open("problem-1.json", mode='r') as f:
    whole_data = json.load(f)

frequency_dict = {}
for twitter in whole_data:
    tags = twitter['entities']['hashtags']
    if len(tags) == 0:
        continue
    for tag in tags:
        if tag['text'] in frequency_dict:
            frequency_dict[tag['text']] = frequency_dict[tag['text']] + 1
        else:
            frequency_dict[tag['text']] = 1

sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))

count = 0
for item in sorted_list:
    print('Top ' + '{:4}'.format(str(count + 1)) + '{:25}'.format(item[0]) + ' ' + str(item[1]) + ' times')
    count = count + 1
    if count == 10:
        break
