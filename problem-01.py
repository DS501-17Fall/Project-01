import json

import twitter
import os


# ---------------------------------------------
# Define a Function to Login Twitter API
def oauth_login():
    # Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information
    # on Twitter's OAuth implementation.

    CONSUMER_KEY = 'THNn3A8S9iEVVoxwujipnwvnt'
    CONSUMER_SECRET = 'cyBdLmR8GpychGE69Co1x1Uw1sgsrs00Yyeye8YipuUBtw4Fsq'
    OAUTH_TOKEN = '1625211115-DgaXEatHXAUOrzKwlPXiwgOFDKA28JoA3xDcx4T'
    OAUTH_TOKEN_SECRET = '5FL2PVPnIz6fRVuQpQdENsGiMusFgQqqMB3XcvOvDv7uN'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


# Define a function to save data in a file
def save_to_file(file_name, data):
    with open(file_name, mode='w') as f:
        f.write(json.dumps(data, indent=2))


# Define a function to save at most max_num of tweets in some topic to a file
def save_topic_to_file(topic, max_num, file_name):
    twitter_stream = twitter.TwitterStream(auth=oauth_login().auth)
    filtered_stream = twitter_stream.statuses.filter(track=topic, language='en')
    data = []
    count = 0
    try:
        for tweet in filtered_stream:
            if max_num <= 0:
                break
            data.append(tweet)
            max_num -= 1
            count += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(count)
    finally:
        print('Gathered ' + str(count) + ' tweets')
        save_to_file(file_name, data)


topic = 'vr'
save_topic_to_file(topic, 200, 'problem-1.json')
