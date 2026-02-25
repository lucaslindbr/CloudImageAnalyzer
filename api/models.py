from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)
    s3_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
