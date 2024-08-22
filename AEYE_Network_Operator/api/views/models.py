from django.db import models

class aeye_ano_models (models.Model):
    whoami    = models.CharField(max_length=40)
    message   = models.CharField(max_length=20)
    image     = models.ImageField(upload_to='images/')
    operation = models.CharField(max_length=40)

    def __str__(self):
        return self.name
