from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, FavouriteBookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'favouritebooks', FavouriteBookViewSet)

urlpatterns = router.urls