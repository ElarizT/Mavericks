import pytest

from faker import Faker
from tests.http_client.AsyncHTTPClient import AsyncHTTPClient

USER_REGISTER_ENDPOINT = "/api/register"

http_client = AsyncHTTPClient(timeout=10)

fake = Faker()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name, password",
    [(fake.user_name(), fake.password())],
    ids=["register user with valid user_name and password"],
)
async def test_users_register(user_name, password):

    json_data = {"password": password, "username": user_name}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[200]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "password",
    [fake.password()],
    ids=["register user without user_name"],
)
async def test_users_register_without_user_name(password):

    json_data = {"password": password}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[422]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name",
    [fake.user_name()],
    ids=["register user without password"],
)
async def test_users_register_without_password(user_name):

    json_data = {"user_name": user_name}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[422]
    )


@pytest.mark.asyncio
async def test_users_register_without_json():

    await http_client.post(path=USER_REGISTER_ENDPOINT, expected_status_codes=[422])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name, password",
    [(fake.user_name(), fake.password())],
    ids=["register two users with same user_name and password"],
)
async def test_users_register_two_users_with_same_user_name_and_password(
    user_name, password
):

    json_data = {"password": password, "username": user_name}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[200]
    )

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[400]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name_1, user_name_2, password",
    [(fake.user_name(), fake.user_name(), fake.password())],
    ids=["register two users with same password"],
)
async def test_users_register_two_users_with_same_password(
    user_name_1, user_name_2, password
):

    json_data = {"password": password, "username": user_name_1}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[200]
    )

    json_data = {"password": password, "username": user_name_2}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[200]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name, password",
    [(fake.user_name(), fake.password())],
    ids=["register user with invalid request body"],
)
async def test_users_register_user_with_invalid_request_body(user_name, password):

    json_data = {"random_stuff": password, "something": user_name}

    await http_client.post(
        path=USER_REGISTER_ENDPOINT, json=json_data, expected_status_codes=[422]
    )
