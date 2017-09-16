import os
from uuid import uuid4
import twitter
import json

'''
usa: geocode='44.467186,-73.214804,2500km'
woeid
usa:23424977
japan:23424856

'''


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


def save_search_to_file(topic, max_num, directory, language='en'):
    if not os.path.exists('./' + directory):
        os.makedirs('./' + directory)
    count = 0
    max_id = -1
    while True:
        if max_id == -1:
            search_result = oauth_login().search.tweets(q=topic, lang=language, count=100)
        else:
            search_result = oauth_login().search.tweets(q=topic, lang=language, count=100,
                                                        max_id=max_id)
        length = len(search_result['statuses'])
        count += length
        if count > max_num or length == 0:
            break
        max_id = search_result['statuses'][length - 1]['id']
        save_to_file(directory + '/' + str(uuid4()) + '.json', search_result['statuses'])
        print('Gathered ' + str(count) + ' data')


'''
If you want the results before some time point, assign topic='YOUR_TOPIC until:2017-01-01'.
If you want the results after some time point, assign topic='YOUR_TOPIC since:2017-01-01'.
Do not forget to change the directory, or your previous results will be mixed with new results.
'''

save_search_to_file(topic='nintendo switch', max_num=10000, directory='switch', language='en')

save_search_to_file(topic='ps4', max_num=10000, directory='ps4', language='en')

save_search_to_file(topic='xbox', max_num=10000, directory='xbox', language='en')
