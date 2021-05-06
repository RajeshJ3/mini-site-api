# django
from rest_framework import views, response, permissions, status
from django.db.models import Q
# apps
from improvements import models as improvements_models
from improvements import serializers as improvements_serializers

# swagger
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

# utils
from improvements import decorators as improvements_decorators
from utils import decorators, responses, utilities


class CreatorViewSet(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = improvements_serializers.CreatorSerializer

    @swagger_auto_schema(
        responses=responses.GET_RESPONSES,
        manual_parameters=[
            openapi.Parameter(name="uuid", in_="query", type=openapi.TYPE_STRING),
        ]
    )
    @decorators.try_except
    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        uuid = query_params.get('uuid', None)

        qs = improvements_models.Creator.objects.filter(
            Q(uuid=uuid) & Q(is_active=True))

        serializer = improvements_serializers.PublicCreatorSerializer(qs, many=True)

        output = {
            "detail": "Successful GET request",
            "output": serializer.data
        }
        return response.Response(output, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses=responses.POST_RESPONSES,
    )
    @decorators.try_except
    def post(self, request):
        data = request.data

        utilities.pop_from_data(['uuid', 'token', 'is_active'], data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            output = {
                "detail": "Successful POST request",
                "output": serializer.data
            }
            return response.Response(output, status.HTTP_200_OK)

        output = {
            "detail": "Unsuccessful POST request",
            "output": serializer.errors
        }
        return response.Response(output, status.HTTP_200_OK)


class EntryViewSet(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = improvements_serializers.EntrySerializer

    @swagger_auto_schema(
        responses=responses.GET_RESPONSES,
        manual_parameters=[
            openapi.Parameter(name="id", in_="query",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(name="token", in_="query",
                              type=openapi.TYPE_STRING),
        ]
    )
    @improvements_decorators.is_creator
    @decorators.try_except
    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        id = query_params.get('id', None)

        creator = kwargs.get("creator")

        qs = improvements_models.Entry.objects.filter(
            Q(is_active=True) & Q(creator=creator))

        if id:
            qs = qs.filter(id=id)

        serializer = self.serializer_class(qs, many=True)

        output = {
            "detail": "Successful GET request",
            "output": serializer.data
        }
        return response.Response(output, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses=responses.POST_RESPONSES,
    )
    def post(self, request):
        data = request.data

        utilities.pop_from_data(['is_active'], data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            output = {
                "detail": "Successful POST request",
            }
            return response.Response(output, status.HTTP_200_OK)

        output = {
            "detail": "Unsuccessful POST request",
            "output": serializer.errors
        }
        return response.Response(output, status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=responses.DELETE_RESPONSES,
        manual_parameters=[
            openapi.Parameter(name="id", in_="query",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(name="token", in_="query",
                              type=openapi.TYPE_STRING),
        ]
    )
    @decorators.try_except
    @improvements_decorators.validate_entry_creator
    def delete(self, request, *args, **kwargs):
        entry = kwargs.get("entry")
        entry.is_active = False
        entry.save()
        details = {
            'message': "Entry successfully deleted",
        }
        return response.Response(details, status.HTTP_200_OK)
