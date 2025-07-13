import pytest

from faker import Faker
from tests.http_client.AsyncHTTPClient import AsyncHTTPClient

USER_REGISTER_ENDPOINT = "/api/register"
LOGIN_ACESS_TOKEN_ENDPOINT = "/api/login/access-token"

http_client = AsyncHTTPClient(timeout=10)

fake = Faker()


# TODO: Add new tests if endpoint is working
@pytest.mark.asyncio
@pytest.mark.skip(reason="Unfinished")
@pytest.mark.parametrize(
    "user_name, password",
    [(fake.user_name(), fake.password())],
    ids=["register valid user and receive acess token"],
)
async def test_users_login_acess_token(user_name, password):

    json_data = {"password": password, "username": user_name}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[200]
    )

    response = await http_client.post(
        path=LOGIN_ACESS_TOKEN_ENDPOINT, json=json_data, expected_status_codes=[200]
    )

    assert response
