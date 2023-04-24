from rest_framework import routers

from borrow.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("", BorrowViewSet, basename="borrow")

urlpatterns = router.urls

app_name = "borrow"
