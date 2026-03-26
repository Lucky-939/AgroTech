from django.db import models

class PestPrediction(models.Model):
    image_name = models.CharField(max_length=255)
    prediction = models.CharField(max_length=50)
    confidence = models.FloatField()
    advisory = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - {self.created_at}"
