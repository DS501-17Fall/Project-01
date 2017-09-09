import json
import operator

# A list of all the tweets collected.
whole_data = []
with open("problem-1.json", mode='r') as f:
    whole_data = json.load(f)

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

sorted_list = reversed(sorted(frequency_dict.items(), key=operator.itemgetter(1)))

count = 0
for item in sorted_list:
    print('Top ' + str(count + 1) + '\t' + str(item[1]) + ' times')
    print(id_text_dict[item[0]] + '\n')
    count += 1
    if count == 10:
        break
