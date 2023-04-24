from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, UserDetailSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
