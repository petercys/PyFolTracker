import argparse
import os
import sys
import json

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

last_followers_list = []
last_followings_list = []
new_followers_list = []
new_followings_list = []

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

with open('./last_followers_list.json', 'r') as f:
    content = f.read()
    last_followers_list = json.loads(content)

with open('./last_followings_list.json', 'r') as f:
    content = f.read()
    last_followings_list = json.loads(content)


my_followings = bot.api.get_total_followers_or_followings(user_id=0,
                                          amount=2000,
                                          which="followings",
                                          to_file="track_followings_abc.json",
                                          overwrite=True,
                                          usernames=True,
                                          filter_private=False,
                                          filter_business=False,
                                          filter_verified=False)

my_followers = bot.api.get_total_followers_or_followings(user_id=0,
                                          amount=2000,
                                          which="followers",
                                          to_file="track_followers_abc.json",
                                          overwrite=True,
                                          usernames=True,
                                          filter_private=False,
                                          filter_business=False,
                                          filter_verified=False)


try:
    my_followings = [item["username"] for item in my_followings]
    my_followers = [item["username"] for item in my_followers]

    new_followers_list = my_followers
    new_followings_list = my_followings
    
    print("\n\nFollowings:")
    for e in last_followings_list:
        if e not in new_followings_list:
            print(e)

    print("\n\nFollowers:")
    for e in last_followers_list:
        if e not in new_followers_list:
            print(e)

    print("\n\n")
finally:
    try:
        os.remove('./last_followers_list.json')
        os.remove('./last_followings_list.json')
    except:
        print('gg')
    
    with open('./last_followers_list.json', 'w+') as f:
        json.dump(list(set(new_followers_list)), f)
    
    with open('./last_followings_list.json', 'w+') as f:
        json.dump(list(set(new_followings_list)), f)
