import pytest
from account.forms import UserPasswordResetForm


@pytest.mark.django_db
def test__user_password_reset_form__email_does_not_exist(user):
    user = user()
    form_data = {
        'email': 'non-existent@email.com',
    }

    form = UserPasswordResetForm(data=form_data)

    assert not form.is_valid()
    assert "This email address doesn't exist" in form.errors['email']


@pytest.mark.django_db
def test__user_password_reset_form__email_exists(user):
    user = user()
    form_data = {
        'email': 'valid@mail.com',
    }

    form = UserPasswordResetForm(data=form_data)

    assert form.is_valid()
    assert not form.errors
