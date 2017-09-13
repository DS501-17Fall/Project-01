import twitter
import json
import os
from uuid import uuid4


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


# trends_result = oauth_login().trends.place(_id=23424977)
# save_to_file('problem-04-trend', trends_result)

def save_search_to_file(topic, max_num, path):
    if not os.path.exists('./' + path):
        os.makedirs('./' + path)
    count = 0
    max_id = -1
    while True:
        if max_id == -1:
            search_result = oauth_login().search.tweets(q=topic, lang='en', count=100)
        else:
            search_result = oauth_login().search.tweets(q=topic, lang='en', count=100, max_id=max_id)
        length = len(search_result['statuses'])
        print('Gathered ' + str(count) + ' data')
        count += length
        if count > max_num or length == 0:
            break
        max_id = search_result['statuses'][length - 1]['id']
        save_to_file(path + '/' + str(uuid4()) + '.json', search_result['statuses'])


topic = 'Ferrari'
save_search_to_file(topic, 1100, 'p4-data')
