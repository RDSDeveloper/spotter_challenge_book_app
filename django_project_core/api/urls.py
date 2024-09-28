from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    AuthorViewSet,
    BookViewSet,
    AddToFavoritesView,
    RemoveFromFavoritesView,
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)

urlpatterns = router.urls + [
    path("favorites/add/", AddToFavoritesView.as_view(), name="add-to-favorites"),
    path(
        "favorites/remove/",
        RemoveFromFavoritesView.as_view(),
        name="remove-from-favorites",
    ),
]
