from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from . signals import save_area_volume

class Box(models.Model):

    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)
    created_by = models.ForeignKey(User,related_name="created_by",on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.pk)
    
    def get_area(self):
        return 2*((self.length * self.width) + (self.width * self.height) + (self.height * self.length))

    def get_volume(self):
        return self.length * self.width * self.height

    def save(self, *args, **kwargs):
        self.area = self.get_area()
        self.volume = self.get_volume()
        self.updated_on = datetime.now()
        super(Box, self).save(*args, **kwargs)

post_save.connect(save_area_volume,sender=Box)