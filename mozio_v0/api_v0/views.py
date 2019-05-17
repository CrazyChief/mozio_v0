import decimal
import re

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

    def list(self, request, *args, **kwargs):
        if 'pos' in request.query_params:
            data = request.query_params.get('pos')
            # parsing of incoming param
            data = re.sub(r'(\[)|(\])|(\s)', '', data)
            pieces = [
                decimal.Decimal(p) for i, p in enumerate(data.split(','))]
            queryset = ServiceArea.objects.filter(
                polygon__contains=[pieces]
            )
            self.serializer_class = FilteredServiceAreaSerializer
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
