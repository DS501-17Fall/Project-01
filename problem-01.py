import os
from uuid import uuid4
import json
import twitter


def oauth_login():
    CONSUMER_KEY = 'THNn3A8S9iEVVoxwujipnwvnt'
    CONSUMER_SECRET = 'cyBdLmR8GpychGE69Co1x1Uw1sgsrs00Yyeye8YipuUBtw4Fsq'
    OAUTH_TOKEN = '1625211115-DgaXEatHXAUOrzKwlPXiwgOFDKA28JoA3xDcx4T'
    OAUTH_TOKEN_SECRET = '5FL2PVPnIz6fRVuQpQdENsGiMusFgQqqMB3XcvOvDv7uN'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


# Define a function to save data in a file
def save_to_file(file_name, data):
    with open(file_name, mode='w') as f:
        f.write(json.dumps(data, indent=2))


# Define a function to save at most max_num of tweets in some topic to a file
def save_topic_to_file(topic, max_num, directory):
    if not os.path.exists('./' + directory):
        os.makedirs('./' + directory)
    count = 1
    while True:
        twitter_stream = twitter.TwitterStream(auth=oauth_login().auth)
        filtered_stream = twitter_stream.statuses.filter(track=topic, language='en')
        while True:
            data = []
            for tweet in filtered_stream:
                if max_num <= 0 < len(data):
                    save_to_file(directory + '/' + str(uuid4()) + '.json', data)
                    return
                data.append(tweet)
                max_num -= 1
                # Save every 50 tweets to a new file
                if len(data) == 50:
                    save_to_file(directory + '/' + str(uuid4()) + '.json', data)
                    break
            print('Gathered ' + str(count * 50) + ' tweets')
            count += 1


save_topic_to_file(topic='trump', max_num=50, directory='p1-data')
