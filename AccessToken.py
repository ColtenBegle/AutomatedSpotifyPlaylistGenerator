class AccessToken:
    token = None
    token_type = None
    expires_in = None
    refresh_token = None
    scope = None

    def __init__(self, token_data_json):
        self.token = token_data_json["access_token"]
        self.token_type = token_data_json["token_type"]
        self.expires_in = token_data_json["expires_in"]
        self.refresh_token = token_data_json["refresh_token"]
