# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupBasedUserRegistrationSerializer
from .serializers import LoginSerializer
from .serializers import LogoutSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class GroupBasedUserRegistrationView(APIView):

    serializer_class = GroupBasedUserRegistrationSerializer
    @swagger_auto_schema(request_body=GroupBasedUserRegistrationSerializer)

    def post(self, request, *args, **kwargs):
        serializer = GroupBasedUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=LoginSerializer)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_tokens(user)
            return Response({
                "message": "Login successful!",
                "tokens": tokens,
                "role": user.role,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    serializer_class = LogoutSerializer
    @swagger_auto_schema(request_body=LogoutSerializer)

    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Logout successful!"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)