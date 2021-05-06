from django.db import models
import uuid


class Creator(models.Model):
    uuid = models.CharField(max_length=32, unique=True, blank=True, null=True)
    token = models.CharField(max_length=32, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            temp_uuid = str(uuid.uuid4()).replace("-", "")[:10]
            while Creator.objects.filter(uuid=temp_uuid).exists():
                temp_uuid = str(uuid.uuid4()).replace("-", "")[:10]
            self.uuid = temp_uuid

        if not self.token:
            temp_token = str(uuid.uuid4()).replace("-", "")
            while Creator.objects.filter(token=temp_token).exists():
                temp_token = str(uuid.uuid4()).replace("-", "")
            self.token = temp_token

        super().save(*args, **kwargs)


class Entry(models.Model):
    creator = models.ForeignKey(
        'improvements.Creator', on_delete=models.CASCADE, related_name='entry_creator')
    name = models.CharField(max_length=100, blank=True, null=True)

    data = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.creator)
