from rest_framework import viewsets,status,serializers,generics
from rest_framework.permissions import IsAuthenticated
from .models import Fitting, Profile
from .serializers import FittingSerializer, ProfileSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

class FittingViewSet(viewsets.ModelViewSet):
    queryset = Fitting.objects.all()
    serializer_class = FittingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)
    
class ScheduleFittingView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        data = request.data
        serializer = FittingSerializer(data=data)
        
        if serializer.is_valid():
            fitting = serializer.save(user=request.user,status='scheduled')
            return Response({'message':'Fitting created', 'status':status.HTTP_201_CREATED, 'fitting':fitting})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileUpdateSet(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        data = request.data
        profile_serializer = ProfileSerializer(data=data)
        user_serializer = UserSerializer(data=data)
        
        if profile_serializer.is_valid():
            profile_serializer.save(user=request.user)
            user_serializer.save(name=request.name)
            return Response({'message':'Profile Updated', 'status':status.HTTP_201_CREATED})
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the user by ID from the URL
        user_id = self.kwargs['pk']
        return User.objects.get(pk=user_id)