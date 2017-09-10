import json

import twitter
import os


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
def save_topic_to_file(topic, max_num, directory):
    if not os.path.exists('./' + directory):
        os.makedirs('./' + directory)
    twitter_stream = twitter.TwitterStream(auth=oauth_login().auth)
    filtered_stream = twitter_stream.statuses.filter(track=topic, language='en')
    count = 1
    while True:
        data = []
        for tweet in filtered_stream:
            if max_num <= 0:
                if len(data) > 0:
                    print('Gathered ' + str((count - 1) * 50 + len(data)) + ' tweets')
                    save_to_file(directory + '/part-' + str(count) + '.json', data)
                return
            data.append(tweet)
            max_num -= 1
            if len(data) == 50:
                save_to_file(directory + '/part-' + str(count) + '.json', data)
                break
        print('Gathered ' + str(count * 50) + ' tweets')
        count += 1


topic = 'trump'
save_topic_to_file(topic, 500, 'data')
