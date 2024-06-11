from django.contrib.auth.views import LoginView

from account.forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'
    extra_context = {'title': 'Авторизация'}
