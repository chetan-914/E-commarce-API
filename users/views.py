from rest_framework import generics, permissions
from .models import User
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer