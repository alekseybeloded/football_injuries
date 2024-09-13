from resources.utils import ExtraContextMixin


def test__extra_context_mixin__title_page_in_context():
    class TestView(ExtraContextMixin):
        title_page = 'Test title page'

    test_view = TestView()
    context = {}
    updated_context = test_view.get_mixin_context(context)

    assert updated_context['title'] == 'Test title page'
