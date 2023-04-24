from rest_framework.permissions import SAFE_METHODS, BasePermission


# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return request.user.is_staff

# class BookList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [AllowAny] # дозволити всім користувачам переглядати список книг без обмежень


# class AllowAny(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return True або ж можна і без цього це built-in method
class BookPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.method == "GET" or (request.user and request.user.is_superuser)