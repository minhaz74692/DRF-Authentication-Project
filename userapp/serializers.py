from rest_framework import serializers
from userapp.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore


from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ( 'password', 'email', 'phone','address' ,'token')

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("The password must be at least 6 characters long.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data.get('email' ),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
        )
        # Generate the token for the newly created user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Save the token in the user table
        user.token = access_token
        user.save()  # Make sure to save the user instance with the new token

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("The new password must be at least 6 characters long.")
        return value
    

class DeleteUserSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=True)

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError("You must confirm to delete your account.")
        return value
