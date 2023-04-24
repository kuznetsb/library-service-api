from rest_framework import routers

from borrow.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("borrows", BorrowViewSet)

urlpatterns = router.urls

app_name = "borrow"
