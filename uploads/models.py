from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='user_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
