from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
# Create your models here.
class HardDrive(models.Model):
    volume = models.IntegerField()

    class Meta:
        db_table = 'harddrive'

class VirtualMachine(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    ram = models.IntegerField()
    cpu = models.IntegerField()
    is_active = models.BooleanField(default=False)
    hd = models.ForeignKey(HardDrive, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = uuid4().hex
        super(VirtualMachine, self).save(*args, **kwargs)