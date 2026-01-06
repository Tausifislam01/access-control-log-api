from django.db import models


class AccessLog(models.Model):
    card_id = models.CharField(max_length=100) # Assignment: physical card identifier (e.g: C1001). Not unique per log entry (a card can appear in many logs). if required as a DB constraint then set unique=True.
    door_name = models.CharField(max_length=100)
    access_granted = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_id} - {self.door_name}"
