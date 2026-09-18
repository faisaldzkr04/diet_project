from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=255)
    carbs = models.FloatField()  # Karbohidrat (gram)
    protein = models.FloatField()  # Protein (gram)
    fat = models.FloatField()  # Lemak (gram)
    fiber = models.FloatField(default=0)  # Serat (gram)
    sodium = models.FloatField(default=0)  # Natrium (mg)

    def __str__(self):
        return self.name
