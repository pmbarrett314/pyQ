import json
import requests


def authenticate(email, password, client_id, client_secret):
    use_password = email is not None and password is not None
    use_client_secret = not use_password and client_id is not None and client_secret is not None

    if use_password:
        token_dict = get_token_email_password(email, password)
    elif use_client_secret:
        token_dict = get_token_client_secret(client_id, client_secret)
    else:
        message = "Either an email/password combination or a client id/secret combination is needed"
        raise NoAuthenticationMethodException(message)

    # TODO: This should raise if authentication info isn't correct

    return token_dict


def get_token_email_password(email, password):
    data = {
        'email': email,
        'password': password,
        'grant_type': 'password'
    }
    return get_token(data)


def get_token_client_secret(client_id, client_secret):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    return get_token(data)


def get_token(data):
    url = "https://q.daskeyboard.com/oauth/1.4/token"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=data, headers=headers)
    try:
        return json.loads(r.content)
    except TypeError:
        return json.loads(r.content.decode('utf-8'))


class NoAuthenticationMethodException(Exception):
    pass
