from django.db import models


class TestModel(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    content = models.TextField()
    meta_info = models.TextField()

