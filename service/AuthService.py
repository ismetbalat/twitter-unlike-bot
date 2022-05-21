from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

class AuthService:
    def __init__(self, credentials):
        self.consumer_key = credentials["consumer_key"]
        self.consumer_key_secret = credentials["consumer_key_secret"]
        self.bearer_token = credentials["bearer_token"]


    def set_auth(self):
        """
        Set authentication for Twitter API
        """
        try:
            # Get request token
            request_token_url = "https://api.twitter.com/oauth/request_token"
            oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_key_secret)

            fetch_response = oauth.fetch_request_token(request_token_url)
            print("Fetch response:", fetch_response)

            resource_owner_key = fetch_response.get("oauth_token")
            resource_owner_secret = fetch_response.get("oauth_token_secret")
            print("Got OAuth token:", resource_owner_key)

            # Get authorization
            base_authorization_url = "https://api.twitter.com/oauth/authorize"
            authorization_url = oauth.authorization_url(base_authorization_url)
            print("Please go here and authorize:", authorization_url)
            verifier = input("Paste the PIN here: ")

            # Get the access token
            access_token_url = "https://api.twitter.com/oauth/access_token"
            oauth = OAuth1Session(
                self.consumer_key,
                client_secret=self.consumer_key_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
                verifier=verifier,
            )
            oauth_tokens = oauth.fetch_access_token(access_token_url)
            print("OAuth tokens:", oauth_tokens)

            access_token = oauth_tokens["oauth_token"]
            access_token_secret = oauth_tokens["oauth_token_secret"]

            oauth = OAuth1Session(
                self.consumer_key,
                client_secret=self.consumer_key_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret,
            )

            return oauth

        except ValueError as e:
            print("There may have been an issue with the consumer_key or consumer_secret you entered:", e)
        except Exception as e:
            print("There was an error:", e)