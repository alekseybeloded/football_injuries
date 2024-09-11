import pytest
from account.forms import UserPasswordChangeForm


@pytest.mark.django_db
def test__user_password_change_form__valid(user):

    form_data = {
        'old_password': user.raw_password,
        'new_password1': 'new_valid_password',
        'new_password2': 'new_valid_password'
    }
    form = UserPasswordChangeForm(user=user, data=form_data)

    assert form.is_valid()

    form.save()

    assert user.check_password('new_valid_password')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'old_password, new_password1, new_password2, expected_error, form_is_valid',
    [
        pytest.param(
            'invalid_old_password',
            'new_valid_password',
            'new_valid_password',
            'Your old password was entered incorrectly. Please enter it again.',
            False,
            id='invalid old password',
        ),
        pytest.param(
            'valid_password',
            'new_invalid_password',
            'new_valid_password',
            'The two password fields didn’t match.',
            False,
            id='invalid new password 1',
        ),
        pytest.param(
            'valid_password',
            'new_valid_password',
            'new_invalid_password',
            'The two password fields didn’t match.',
            False,
            id='invalid new password 2',
        ),
    ]
)
def test__user_password_change_form__invalid(
    user,
    old_password,
    new_password1,
    new_password2,
    expected_error,
    form_is_valid
):
    form_data = {
        'old_password': old_password,
        'new_password1': new_password1,
        'new_password2': new_password2,
    }
    form = UserPasswordChangeForm(user=user, data=form_data)

    assert form.is_valid() == form_is_valid
    assert expected_error in str(form.errors)
