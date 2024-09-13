import pytest
from account.forms import UserRegistrationForm
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test__user_registration_form__valid():
    form_data = {
        'username': 'new_valid_username',
        'email': 'new_valid@mail.com',
        'password1': 'valid_password',
        'password2': 'valid_password',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
    }
    form = UserRegistrationForm(data=form_data)

    assert form.is_valid()

    form.save()

    assert get_user_model().objects.filter(username='new_valid_username').exists()


@pytest.mark.django_db
def test__user_registration_form__invalid_email_exists(user):
    form_data = {
        'username': 'new_valid_username',
        'email': user.email,
        'password1': 'new_valid_password',
        'password2': 'new_valid_password'
    }
    form = UserRegistrationForm(data=form_data)

    assert not form.is_valid()
    assert 'This email already exists' in form.errors['email']
