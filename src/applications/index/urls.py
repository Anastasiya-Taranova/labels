from django.urls import path

from applications.index.apps import IndexConfig
from applications.index.views import IndexView

app_name = IndexConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
