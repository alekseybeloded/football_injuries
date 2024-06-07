menu = [
    {'title': 'Добавить игрока', 'url_name': 'add_player'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'Что-нибудь еще', 'url_name': 'login'},
]


class MenuMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context.update(kwargs)
        return context
