from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class MenuItem:
    title: str
    url_name: str


menu = [MenuItem(title='Contacts', url_name='contacts')]


class ExtraContextMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        context.update(self.extra_context)
        context.update(kwargs)
        return context
