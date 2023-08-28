from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class MPrint(models.Model):
    print_name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    price = models.IntegerField()
    info = models.CharField(max_length=200)
    color = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True, default='/model3d.png')

    def __str__(self):
        return self.print_name + " " + self.desc
