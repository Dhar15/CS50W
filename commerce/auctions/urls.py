from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("create", views.create, name="create"),
    path("watchlistpage/<str:username>",views.watchlistpage,name="watchlistpage"),
    path("listings/<int:id>",views.listingpage,name="listingpage"),
    path("addtowatchlist/<int:list_id>", views.addtowatchlist, name="addtowatchlist"),
    path("removefromwatchlist/<int:list_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("categories", views.categories, name="categories"),
    path("<str:category>/jumptocategory", views.jumptocategory, name="jumptocategory"),
    path("<int:list_id>", views.list, name="list"),
    path("add_comment/<int:list_id>", views.add_comment, name="add_comment"),
    path("delete_cmt/<int:list_id>", views.delete_cmt, name="delete_cmt"),
    path("add_bid/<int:list_id>", views.add_bid, name="add_bid"),
    path("close_bid/<int:list_id>", views.close_bid, name="close_bid"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
