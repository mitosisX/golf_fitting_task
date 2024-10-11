from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Fitting

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id','username','user','email','address', 'phone', 'golf_club_size']


class UserSerializer2(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = [ 'username', 'address', 'phone', 'email', 'profile']
        
    def update(self, instance, validated_data):
        # Update user email
        email = validated_data.pop('email', None)
        if email is not None:
            instance.email = email
        
        # Update profile data
        profile_data = validated_data.pop('profile', {})
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
        
        instance.save()

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ('username', 'email','profile')
        
    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        if email is not None:
            instance.email = email
        
        profile_data = validated_data.pop('profile', {})
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
        
        instance.save()
        return instance

class FittingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Fitting
        fields = ['id','user','date', 'time', 'comments', 'status']
        # fields= "__all__"