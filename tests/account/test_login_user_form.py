import pytest
from account.forms import LoginUserForm


@pytest.mark.django_db
def test__login_user_form__valid(user):
    form_data = {'username': user.username, 'password': user.raw_password}
    form = LoginUserForm(data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test__login_user_form__invalid():
    form_data = {'username': 'invalid_username', 'password': 'invalid_password'}
    form = LoginUserForm(data=form_data)

    assert not form.is_valid()
    assert 'Please enter a correct username/email and password' in form.errors['__all__'][0]
