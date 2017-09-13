import twitter
from prettytable import PrettyTable


def oauth_login():
    CONSUMER_KEY = 'THNn3A8S9iEVVoxwujipnwvnt'
    CONSUMER_SECRET = 'cyBdLmR8GpychGE69Co1x1Uw1sgsrs00Yyeye8YipuUBtw4Fsq'
    OAUTH_TOKEN = '1625211115-DgaXEatHXAUOrzKwlPXiwgOFDKA28JoA3xDcx4T'
    OAUTH_TOKEN_SECRET = '5FL2PVPnIz6fRVuQpQdENsGiMusFgQqqMB3XcvOvDv7uN'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


twitter_api = oauth_login()
friends = twitter_api.friends.ids(screen_name='LucaMWayne')
friend_list = []
for id in friends['ids']:
    friend_list.append((id, twitter_api.users.lookup(user_id=id)[0]['screen_name']))
friend_table = PrettyTable(['id', 'screen_name'])
for row in friend_list:
    friend_table.add_row(row)
print('Friend Table')
print(friend_table)

followers = twitter_api.followers.ids(screen_name='LucaMWayne')
follower_list = []
for id in followers['ids']:
    follower_list.append((id, twitter_api.users.lookup(user_id=id)[0]['screen_name']))
follower_table = PrettyTable(['id', 'screen_name'])
for row in follower_list:
    follower_table.add_row(row)
print('Follower Table')
print(follower_table)

mutual_list = []
for item in friend_list:
    if item in follower_list:
        mutual_list.append(item)
mutual_table = PrettyTable(['id', 'screen_name'])
for row in mutual_list:
    mutual_table.add_row(row)
print('Mutual Table')
print(mutual_table)
