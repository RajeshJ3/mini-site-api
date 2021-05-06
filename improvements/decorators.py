from django.db.models import Q
from rest_framework import response, status
from improvements import models as improvements_models


##############################################
#               Validate Objects             #
##############################################
def validate_entry(func):
    def check(*args, **kwargs):

        request = args[1]

        if request.query_params.get('id', 0):
            id = request.query_params.get('id', 0)
        else:
            id = request.data.get('id', 0)

        if not id:
            return response.Response({'message': 'id is not passed'}, status.HTTP_400_BAD_REQUEST)

        entries = improvements_models.Entry.objects.filter(
            Q(id=id) & Q(is_active=True))

        if not len(entries):
            return response.Response({'message': 'Invalid id'}, status.HTTP_400_BAD_REQUEST)

        kwargs.update({"entry": entries.first()})

        return func(*args, **kwargs)

    return check


##############################################
#               Validate Users               #
##############################################
def is_creator(func):
    def check(*args, **kwargs):

        request = args[1]

        if request.query_params.get('token', 0):
            token = request.query_params.get('token', 0)
        else:
            token = request.data.get('token', 0)

        if not token:
            return response.Response({'message': 'token is not passed'}, status.HTTP_400_BAD_REQUEST)

        creators = improvements_models.Creator.objects.filter(
            Q(token=token) & Q(is_active=True))

        if not len(creators):
            return response.Response({'message': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)

        kwargs.update({"creator": creators.first()})

        return func(*args, **kwargs)

    return check


def validate_entry_creator(func):
    @is_creator
    @validate_entry
    def check(*args, **kwargs):
        creator = kwargs.get("creator")
        entry = kwargs.get("entry")

        if entry.creator == creator:
            return func(*args, **kwargs)

        return response.Response({'message': 'Permission denied, invalid user'}, status.HTTP_400_BAD_REQUEST)

    return check
