from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255)
    text = models.TextField()
