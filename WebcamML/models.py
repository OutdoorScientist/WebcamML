from django.db import models

# Create your models here.
class WebcamPic(models.Model):
    title = models.CharField(max_length=120)
    # screenshot = models.ImageField(upload_to='pictures')