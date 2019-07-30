from django.db import models

# Create your models here.

class AppUsageLog(models.Model):
    app = models.CharField(max_length=64)
    rx  = models.IntegerField()
    tx  = models.IntegerField()
    ts = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{}/{}/{}".format(self.app,self.rx,self.tx)
