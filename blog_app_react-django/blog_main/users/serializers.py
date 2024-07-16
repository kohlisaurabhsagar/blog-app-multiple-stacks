from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'fname', 'lname', 'profile_image']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'fname', 'lname', 'password']

    @sync_to_async
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            fname=validated_data['fname'],
            lname=validated_data['lname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    
class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        raise serializers.ValidationError('Invalid credentials')
