from django.db import models


class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
