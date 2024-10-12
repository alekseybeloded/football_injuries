import pytest
from account.forms import UserProfileForm


@pytest.mark.django_db
def test__user_profile_form__valid(user):
    user = user()
    form_data = {
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
