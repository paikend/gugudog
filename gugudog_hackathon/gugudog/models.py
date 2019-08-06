from django.db import models
from django.conf import settings

CATEGORY_CHOICES = (
    ('music', '음악'),
    ('clothing', '의류'),
    ('media', '영상')
)

# Create your models here.
interestChoice = (
    ('FAHION', '패션'),
    ('MEDIA', '미디어'),
    ('FOOD', '음식'),
    ('ETC', '기타'),
)

class Category(models.Model):
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)
    price = models.IntegerField()
    link = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)

    full_name = models.OneToOneField(
      'self', on_delete=models.CASCADE, null=True, blank=True)
   # category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    image = models.ImageField(upload_to='logo_images', null=True, blank=True)
# @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    gudog_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="gudog_users",
    )

    zzim_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="zzim_users",
    )

    def get_price(self):
        return format(self.price, ',')

    def __str__(self):
        return f"{self.company} {self.service_name} (+{self.price}원)"


class GuDogService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    register_date = models.DateTimeField(null=True, blank=True)

    # def get_total(self):
    #     services = self.objects.all()
    #     for servic
    #     total_price = 0
    #     for service in services:
    #         total_price += service.price
        
        # return total_price

    def __str__(self):
        return f"{self.user} {self.service}"       

class ZzimService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ZZservice",
    )

    def __str__(self):
        return f"{self.service}"    

class GuDog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    services = models.ManyToManyField(GuDogService)

    def __str__(self):
        return self.user.username

class Zzim(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    services = models.ManyToManyField(ZzimService)

    def __str__(self):
        return self.user.username

class InterestService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    interest_cate = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # related_name='interest_category'
    )

    def __str__(self):
        return f"{self.interest_cate}"    

class Interest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    interests = models.ManyToManyField(InterestService)

    def __str__(self):
        return self.user.username