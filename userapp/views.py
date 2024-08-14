from django.shortcuts import render
from userapp.serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer, DeleteUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from userapp.models import CustomUser

class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            print("This is data type of user: ", type(user))
            if user:
                return Response({
                        "user_data": user_serializer.data,
                    }, status=status.HTTP_201_CREATED)
            return Response({
                        "message":"Error in sign up",
                    }, status=status.HTTP_403_FORBIDDEN)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Update the user's token in the database
            user.token = access_token
            user.save()  # Save the updated user instance

            print("This is your access token:", access_token)

            return Response({"message": "Succesfully Loged In", "token": access_token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserList(APIView):
    def get(self, request):
        if request.method == "GET":
            users = CustomUser.objects.all().order_by('-id') #use '-id' for descending order return
            # serializer = UserSerializer({}, many = False)
            if users:
                userData = []
                for user in users:
                    emptyMap = {}
                    emptyMap['id'] = user.id
                    emptyMap['email'] = user.email
                    emptyMap['phone'] = user.phone
                    emptyMap['address'] = user.address
                    emptyMap['date_joined'] = user.date_joined
                    userData.append(emptyMap)

                serializer = UserSerializer(users, many = True)
                return Response(userData, status= status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.delete()
            return Response({"detail": "User account deleted successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
