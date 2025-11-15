from rest_framework import generics, status
from . import serializers
from utils import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny] #Allow anyone to register

    def create(self, request, *args, **kwargs):
        """serialize the data and manually return a custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            "message": f"Your account has been succesfully created",
            "user_details": {
                "id": f"{user.id}",
                "email": f"{user.email}",
                "role": f"{user.role}"
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user