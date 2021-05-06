from rest_framework import serializers
from improvements import models

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creator
        fields = "__all__"


class PublicCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creator
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = {
            "id": data.get("id"),
            "name": data.get("name"),
        }
        return data


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = "__all__"

