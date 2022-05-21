from service.AuthService import AuthService
from service.LikeService import LikeService
from service.UserService import UserService
import json

credentials = {
    "consumer_key": "xxxxxxxxxxxxx",
    "consumer_key_secret": "xxxxxxxxxxxxx",
    "bearer_token": "xxxxxxxxxxxxx"
}

try:
    authService = AuthService(credentials)
    oauth = authService.set_auth()

    # Service init
    userService = UserService(oauth)
    likeService = LikeService(oauth, credentials["bearer_token"])

    # Get my information
    user_me = userService.get_user_me()
    print(json.dumps(user_me, indent=4, sort_keys=True))

    # Get user information by id
    user_by_id = userService.get_user_by_id(user_me["data"]["id"])
    print(json.dumps(user_by_id, indent=4, sort_keys=True))

    # Get user information by username
    user_by_username = userService.get_user_by_username(user_me["data"]["username"])
    print(json.dumps(user_by_username, indent=4, sort_keys=True))

    # Get liked tweets by user id
    likeService.liked_tweets_request_limit = 1
    liked_tweets = likeService.get_liked_tweets(user_me["data"]["id"])
    print("Liked tweets:", liked_tweets)
    print("Liked tweets count:", len(liked_tweets))

    # Unlike a tweet
    for tweet_id in liked_tweets:
        print(liked_tweets[tweet_id])
        response = likeService.unlike_tweet(user_me["data"]["id"], tweet_id)
        print(response)
        print("-"*50)
    

except Exception as e:
    print(e)