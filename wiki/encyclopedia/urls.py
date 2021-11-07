from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:q>", views.search, name = "search"),
    path("results/<str:q>/", views.results, name = "results"),
    path("newpage/", views.npage, name="newpage"),
    path("random/", views.rpage, name="randompage"),
    path("<str:q>/edit", views.edit, name="edit")
]
