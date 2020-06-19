from django.urls import path
from django.views.generic import View

urlpatterns = [
    path("simple/action/", View.as_view(), name="simpleAction"),
]
