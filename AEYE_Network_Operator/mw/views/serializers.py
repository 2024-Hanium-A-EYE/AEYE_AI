from rest_framework import serializers
from .models import aeye_inference_models, aeye_train_models, aeye_test_models

class aeye_inference_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_inference_models
        fields = ['whoami', 'image', 'message']

class aeye_train_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_train_models
        fields = ['whoami', 'message']

class aeye_test_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_test_models
        fields = ['whoami', 'message']