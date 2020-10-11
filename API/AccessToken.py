class AccessToken:
    user_id = None
    token = None
    token_type = None
    expires_in = None
    refresh_token = None
    scope = None

    def __init__(self, user_id, token_data_dict):
        self.user_id = user_id
        self.token = token_data_dict["access_token"]
        self.token_type = token_data_dict["token_type"]
        self.expires_in = token_data_dict["expires_in"]
        self.refresh_token = token_data_dict["refresh_token"]
        self.scope = token_data_dict["scope"]
