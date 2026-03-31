import pytest
import requests


@pytest.fixture(scope='module')
def soap_session(envs):
    session = requests.Session()
    session.base_url = envs.soap_address
    session.headers.update({
        "Content-Type": "text/xml; charset=utf-8"
    })
    return session
