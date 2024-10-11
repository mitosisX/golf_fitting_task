from rest_framework import serializers
from .models import GettingStartedInfo
from consumer.models import Fitting
from consumer.serializers import UserSerializer

class GettingStartedInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GettingStartedInfo
        fields = ['content']
        

class FittingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Fitting
        fields = '__all__'