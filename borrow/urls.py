from django.urls import path, include
from rest_framework import routers

from borrow.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("", BorrowViewSet, basename="borrowings")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/return/", BorrowViewSet.as_view({"patch": "return_borrow"}), name="return_borrow"),
]

app_name = "borrow"
