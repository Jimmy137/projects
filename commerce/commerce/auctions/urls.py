from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.crl, name="crl"),
    path("listing/<int:lid>", views.lst, name="list"),
    path("category/<int:cid>", views.category, name="category"),
    path("categories", views.categories , name="categories"),
    path('listing/<int:lid>/comment/', views.comment , name="comment"),
    path('listing/<int:lid>/bid/' , views.bid , name="bid"),
    path('user/<int:uid>/w/' , views.watch , name="watch"),
    path('listing/<int:lid>/w/' , views.addwatch, name="addwatch"),
    path('listing/<int:lid>/close/' , views.close, name="close"),
    path('listing/<int:lid>/remove/' , views.remove, name="remove")

 ]
