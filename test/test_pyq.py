import os
import pytest

from pyq import main, NoAuthenticationMethodException


class CleanEnv():
    def __init__(self, keys):
        self.keys = keys
        self.tmp_dict = {}

    def __enter__(self):
        for key in self.keys:
            if key in os.environ:
                self.tmp_dict[key] = os.environ.get(key)
                del os.environ[key]

    def __exit__(self, *args):
        for key in self.keys:
            if key in self.tmp_dict:
                os.environ[key] = self.tmp_dict[key]


def test_empty_auth():
    with CleanEnv(["PYQ_CLIENT_ID", "PYQ_CLIENT_SECRET", "PYQ_PASSWORD", "PYQ_EMAIL"]):
        with pytest.raises(NoAuthenticationMethodException):
            main(["auth"])


def test_key_auth():
    client_id = os.environ.get("PYQ_CLIENT_ID")
    client_secret = os.environ.get("PYQ_CLIENT_SECRET")
    with CleanEnv(["PYQ_CLIENT_ID", "PYQ_CLIENT_SECRET", "PYQ_PASSWORD", "PYQ_EMAIL"]):
        key_dict = main(["--client_id", client_id, "--client_secret", client_secret, "auth"])
    assert "access_token" in key_dict
    assert "refresh_token" in key_dict
    assert "user_id" in key_dict


def test_password_auth():
    email = os.environ.get("PYQ_EMAIL")
    password = os.environ.get("PYQ_PASSWORD")
    with CleanEnv(["PYQ_CLIENT_ID", "PYQ_CLIENT_SECRET", "PYQ_PASSWORD", "PYQ_EMAIL"]):
        key_dict = main(["--email", email, "--password", password, "auth"])
    assert "access_token" in key_dict
    assert "refresh_token" in key_dict
    assert "user_id" in key_dict
