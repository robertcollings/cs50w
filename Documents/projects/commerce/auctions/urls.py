from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:auction_id>", views.view_listing, name="view-listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch/<int:listing>", views.watch, name="watch"),
    path("unwatch/<int:listing>", views.unwatch, name="unwatch"),
    path("endlisting/<int:listing>", views.end, name="end"),
    path("category/<str:cat>", views.category, name="category"),
]
