import datetime
import json
from AccessToken import AccessToken


def store_access_token(access_token):
    if not (access_token.token is None):
        try:
            data = f"<RECORD>\n\t{access_token.token}, {access_token.token_type}, {access_token.expires_in}, " \
                   f"{access_token.refresh_token}, {access_token.scope}\n<RECORD>\n"
            with open("%AppData%/TokenData.txt", "a") as file:
                file.write(data)
        except OSError as osErr:
            print(osErr.errno, osErr.strerror, osErr.filename)
    else:
        print("No valid access token given. Cannot store it in file.")


def get_good_access_token():
    try:
        records = []
        with open("%AppData%/TokenData.txt") as file:
            data = file.read()
            for line in data:
                if not (line == "<RECORD>"):
                    records.append(line)

        for record in records:
            expires = datetime.datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S.%f")
            if expires > datetime.datetime.now():
                token_json = token_data_to_json(record[0], record[1], record[2], record[3], record[4])
                access_token = AccessToken(token_json)
                return access_token

    except OSError as osErr:
        print(osErr.errno, osErr.strerror, osErr.filename)


def token_data_to_json(token, token_type, expires_in, refresh_token, scope):
    token_dict = {
        "access_token": token,
        "token_type": token_type,
        "expires_in": expires_in,
        "refresh_token": refresh_token,
        "scope": scope
    }
    token_json = json.dumps(token_dict)
    return token_json


def purge_access_tokens():
    pass
