from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UpdateUserSerializer, UpdatePassSerializer
from knox.views import LogoutView

# Register API


class RegisterUserApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Get user API
class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Update user API
class UpdateUserAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


# Update user API
class UpdatePassAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UpdatePassSerializer

    def get_object(self):
        return self.request.user


# Logout API
class LogoutAPI(LogoutView):
    pass
