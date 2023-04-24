from django.urls import path, include
from rest_framework import routers

from book.views import BookViewSet

router = routers.DefaultRouter()
router.register("", BookViewSet, basename="books")

urlpatterns = router.urls

app_name = "book"
