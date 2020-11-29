from django.views.generic import ListView

from applications.index.models import AuthModel


class IndexView(ListView):
    model = AuthModel
    context_object_name = 'users'
    template_name = "index/index.html"
