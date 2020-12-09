from django.views.generic import ListView

from applications.index.models import AuthModel
from applications.index.utils.labels import delete_label


class IndexView(ListView):
    model = AuthModel
    context_object_name = "users"
    template_name = "index/index.html"

    # def get_context_data(self, *args, **kwargs):
    #     results = delete_label()
    #     if results is None:
    #         print("ploxo")
    #     ctx = super().get_context_data(*args, **kwargs)
    #     ctx.update(
    #         {
    #             "all_info": results,
    #         }
    #     )
    #
    #     return ctx
