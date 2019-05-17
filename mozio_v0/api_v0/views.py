from django.db.models import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from providers.models import Provider, ServiceArea

from .serializers import (ProviderSerializer, ServiceAreaSerializer,
                          FilteredServiceAreaSerializer)


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Provider objects
    """

    queryset = Provider.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ServiceArea objects
    """

    queryset = ServiceArea.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ServiceAreaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pc = self.perform_create(serializer)
        if 'Error' in pc.keys():
            return Response(pc, status=status.HTTP_409_CONFLICT)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(
                pc, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        data = self.request.data
        try:
            provider = Provider.objects.get(pk=data['provider'])
        except ObjectDoesNotExist:
            provider = False
        if provider is False:
            return {
                'Error': 'Current provider does not exist'
            }
        if len(data['polygon']) < 3:
            return {
                'Error': '"polygon" param must have length greater than 2'
            }
        for i, part in enumerate(data['polygon']):
            if len(part) != 2:
                return {
                    'Error': 'Provide correct pairs of coordinates.'
                }
        service_area = serializer.save()
        service_area.provider = provider
        service_area.save()
        return {
            'Success': 'New ServiceArea successfully created!'
        }
