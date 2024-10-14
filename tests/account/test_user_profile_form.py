import pytest
from account.forms import UserProfileForm


@pytest.mark.django_db
def test__user_profile_form__valid(user):
    user = user()
    form_data = {
        'username': user.username,
        'email': user.email,
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
    }

    form = UserProfileForm(instance=user, data=form_data)

    assert form.is_valid()

    form.save()
    user.refresh_from_db()

    assert user.first_name == 'new_first_name'
    assert user.last_name == 'new_last_name'
    assert user.username == 'valid_username'
    assert user.email == 'valid@mail.com'


@pytest.mark.django_db
def test__user_profile_form__email_already_exists(user):
    first_user = user()
    second_user = user(username='another_valid_username', email='another_valid_email@mail.com')
    form_data = {
        'username': first_user.username,
        'email': second_user.email,
        'first_name': first_user.first_name,
        'last_name': first_user.last_name,
    }

    form = UserProfileForm(instance=first_user, data=form_data)

    assert not form.is_valid()
    assert 'This email already exists' in form.errors['email']


@pytest.mark.django_db
def test__user_profile_form__username_already_exists(user):
    first_user = user()
    second_user = user(username='another_valid_username', email='another_valid_email@mail.com')
    form_data = {
        'username': second_user.username,
        'email': first_user.email,
        'first_name': first_user.first_name,
        'last_name': first_user.last_name,
    }

    form = UserProfileForm(instance=first_user, data=form_data)

    assert not form.is_valid()
    assert 'This username already exists' in form.errors['username']

