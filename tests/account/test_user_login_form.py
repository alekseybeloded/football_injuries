import pytest
from account.forms import UserLoginForm


@pytest.mark.django_db
def test__user_login_form__valid(user):
    user = user()
    form_data = {'username': user.username, 'password': user.raw_password}
    form = UserLoginForm(data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test__user_login_form__invalid():
    form_data = {'username': 'invalid_username', 'password': 'invalid_password'}
    form = UserLoginForm(data=form_data)

    assert not form.is_valid()
    assert 'Please enter a correct username/email and password' in form.errors['__all__'][0]
