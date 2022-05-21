import requests
import json

class LikeService:
    def __init__(self, oauth, bearer_token):
        self.oauth = oauth
        self.bearer_token = bearer_token
        self.liked_tweets_request_count = 0
        self.liked_tweets_request_limit = 1
    
    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2LikedTweetsPython"
        return r

    def create_url(self, user_id, next_token = None):
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        tweet_fields = "tweet.fields=id,author_id,text"

        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        if (next_token is None):
            url = "https://api.twitter.com/2/users/{}/liked_tweets".format(user_id)
        else:
            url = "https://api.twitter.com/2/users/{}/liked_tweets".format(user_id)
            url += "?pagination_token={}".format(next_token)
        
        return url, tweet_fields


    def get_liked_tweets(self, user_id, next_token = None):
        """
        Get liked tweets by user id
        Every request it gets 100 liked tweets
        Default request limit for API: 75 requests / 15 mins
        """
        liked_tweets = {}

        if self.liked_tweets_request_count != self.liked_tweets_request_limit:
            self.liked_tweets_request_count += 1
            
            if (next_token is None):
                url, tweet_fields = self.create_url(user_id)
            else:
                url, tweet_fields = self.create_url(user_id, next_token)
            
            response = requests.request("GET", url, auth=self.bearer_oauth, params=tweet_fields)
            
            if response.status_code != 200:
                raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
            
            tweets = response.json()

            for tweet in tweets["data"]:
                liked_tweets[tweet["id"]] = tweet["text"]

            if tweets["meta"]["next_token"] != None:
                tweets = self.get_liked_tweets(user_id, next_token = tweets["meta"]["next_token"])
                liked_tweets = liked_tweets | tweets
            
            print("Response code: {}".format(response.status_code))

        return liked_tweets

    def unlike_tweet(self, user_id, tweet_id):
        """
        Unlike a tweet
        """
        url = "https://api.twitter.com/2/users/{}/likes/{}".format(user_id, tweet_id)
        response = self.oauth.delete(url)
        
        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
        
        print("Response code: {}".format(response.status_code))
        
        return response.json()