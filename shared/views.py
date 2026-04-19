from django.views.generic import TemplateView
from posts.models import Post

class HomepageView(TemplateView):
    template_name = "shared/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context