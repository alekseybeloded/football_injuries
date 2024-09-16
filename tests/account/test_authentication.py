import pytest
from django.test import RequestFactory
from django.urls import reverse


def test__authentication__valid_email_and_password(user, email_auth_backend):
    request = RequestFactory().post(reverse('account:login'))
    authenticated_user = email_auth_backend.authenticate(
        request,
        username=user.email,
        password=user.raw_password
    )

    assert authenticated_user is not None
    assert authenticated_user == user


@pytest.mark.parametrize(
    'email, password, expected_result',
    [
        pytest.param(
            'invalid email',
            'valid_password',
            None,
            id='invalid email',
        ),
        pytest.param(
            'valid@mail.com',
            'invalid_password',
            None,
            id='invalid password',
        ),
    ]
)
def test__authentication__invalid(user, email_auth_backend, email, password, expected_result):
    request = RequestFactory().post(reverse('account:login'))
    authenticated_user = email_auth_backend.authenticate(
        request,
        username=email,
        password=password
    )

    assert authenticated_user is expected_result


def test__get_user__valid_id(user, email_auth_backend):
    fetched_user = email_auth_backend.get_user(user.id)

    assert fetched_user is not None
    assert fetched_user == user


def test__get_user__invalid_id(user, email_auth_backend):
    fetched_user = email_auth_backend.get_user(111)

    assert fetched_user is None
