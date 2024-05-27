# myapp/serializers.py
from rest_framework import serializers

class DocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50)
    )
