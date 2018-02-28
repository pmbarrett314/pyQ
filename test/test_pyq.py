import pytest
from pyq import main, NoAuthenticationMethodException


def test_empty_auth():
    with pytest.raises(NoAuthenticationMethodException):
        main(["auth"])
