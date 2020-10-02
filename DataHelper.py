import datetime
import json
from AccessToken import AccessToken


def store_access_token(access_token):
    if not (access_token.token is None):
        try:
            data = f"{access_token.user_id}, {access_token.token}, " \
                   f"{access_token.token_type}, {access_token.expires_in}, " \
                   f"{access_token.refresh_token}, {access_token.scope}"
            with open("%AppData%/TokenData.txt", "a") as file:
                file.write(data)
        except OSError as osErr:
            print(osErr.errno, osErr.strerror, osErr.filename)
    else:
        print("No valid access token given. Cannot store it in file.")


def get_good_access_token(user_id):
    try:
        records = []
        purge_outdated_access_tokens()
        with open("%AppData%/TokenData.txt", "r") as file:
            tmprecords = file.readlines()
            for record in tmprecords:
                data = record.split(", ")
                records.append(data)
        for record in records:
            if record[0] == user_id:
                record_dict = get_record_dict(record)
                access_token = AccessToken(record[0], record_dict)
                return access_token
            else:
                print(f"No access tokens found for user: {user_id}")
                return None
    except OSError as osErr:
        print(osErr.errno, osErr.strerror, osErr.filename)


def get_record_dict(record):
    record_dict = {
        "access_token": record[1],
        "token_type": record[2],
        "expires_in": record[3],
        "refresh_token": record[4],
        "scope": record[5]
    }
    return record_dict


def purge_outdated_access_tokens():
    try:
        records = []
        with open("%AppData%/TokenData.txt", "r+") as file:
            tmprecords = file.readlines()
            for record in tmprecords:
                data = record.split(", ")
                records.append(data)
            file.write("")  # Clear file
        with open("%AppData%/TokenData.txt", "a") as file:
            for record in records:
                print(record)
                expires = datetime.datetime.strptime(record[3], "%Y-%m-%d %H:%M:%S")
                data = f"{record[0]}, {record[1]}, {record[2]}, " \
                       f"{record[3]}, {record[4]}, {record[5]}"
                if expires > datetime.datetime.now():  # Add useful tokens only
                    file.write(data)
    except OSError as osErr:
        print(osErr.errno, osErr.strerror, osErr.filename)
