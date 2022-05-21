class UserService:
    def __init__(self, oauth):
        self.oauth = oauth

    def get_user_me(self):
        """
        Get my information
        """
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        fields = "id,name,username,created_at,description"
        params = {"user.fields": fields}

        response = self.oauth.get("https://api.twitter.com/2/users/me", params=params)

        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

        print("Response code: {}".format(response.status_code))

        return response.json()


    def get_user_by_id(self, user_id):
        """
        Get user information by id
        """
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        fields = "id,name,username,created_at,description"
        params = {"user.fields": fields}

        response = self.oauth.get("https://api.twitter.com/2/users/{}".format(user_id), params=params)

        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

        print("Response code: {}".format(response.status_code))

        return response.json()


    def get_user_by_username(self, username):
        """
        Get user information by username
        """
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        fields = "id,name,username,created_at,description"
        params = {"user.fields": fields}

        response = self.oauth.get("https://api.twitter.com/2/users/by/username/{}".format(username), params=params)

        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

        print("Response code: {}".format(response.status_code))

        return response.json()