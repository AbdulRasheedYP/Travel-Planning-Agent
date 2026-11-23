from django.db import models
from pgvector.django import VectorField


class TravelKnowledge(models.Model):
    destination = models.CharField(max_length=100)

    content = models.TextField()

    embedding = VectorField(dimensions=3072)

    source = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination