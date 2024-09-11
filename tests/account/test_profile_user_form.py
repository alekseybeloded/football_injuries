import pytest
from account.forms import ProfileUserForm


@pytest.mark.django_db
def test__profile_user_form__valid(user):
    form_data = {
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
    }

    form = ProfileUserForm(instance=user, data=form_data)

    assert form.is_valid()

    form.save()
    user.refresh_from_db()

    assert user.first_name == 'new_first_name'
    assert user.last_name == 'new_last_name'
    assert user.username == 'valid_username'
    assert user.email == 'valid@mail.com'
