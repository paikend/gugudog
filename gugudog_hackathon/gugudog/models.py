from django.db import models
from django.conf import settings

CATEGORY_CHOICES = (
    ('music', '음악'),
    ('clothing', '의류'),
    ('media', '영상')
)

# Create your models here.
class Service(models.Model):
    company = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)
    price = models.IntegerField()
    link = models.CharField(max_length=500)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    # logo = models.FileField()

    def __str__(self):
        return self.company + " " + self.service_name

class GuDogService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    # register_date = models.DateTimeField()


    def __str__(self):
        return str(self.user) + " " + str(self.service.service_name)

class GuDog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    services = models.ManyToManyField(GuDogService)