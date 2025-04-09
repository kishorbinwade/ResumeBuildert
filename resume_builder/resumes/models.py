from django.db import models

# Create your models here.
import uuid
from django.db import models

class Resume(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    data = models.JSONField()  # Store form data as JSON