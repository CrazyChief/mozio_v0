from rest_framework import serializers

from providers.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = (
            'name',
            'email',
            'phone_number',
            'language',
            'currency',
        )


class ServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea
        fields = (
            'polygon_name',
            'price',
            'polygon',
        )
