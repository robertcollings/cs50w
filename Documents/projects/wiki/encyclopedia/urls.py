from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new-page"),
    path("edit-page/<str:name>", views.edit_page, name="edit-page"),
    path("delete/<str:name>", views.delete, name="delete"),
    path("randompg", views.randompg, name="random")
]
