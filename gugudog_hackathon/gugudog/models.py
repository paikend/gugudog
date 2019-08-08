from django.db import models
from django.conf import settings

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

    image = models.ImageField(upload_to='logo_images', null=True, blank=True)

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

    # 서비스를 구독하는 유저의 수
    def get_gudog_users(self):
        return self.gudog_users.all().count()

    # 서비스를 찜한 유저의 수
    def get_zzim_users(self):
        return self.zzim_users.all().count()

    def __str__(self):
        return self.company + " " + self.service_name + " (+" + str(self.price) + "원)"


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

    def __str__(self):
        return self.user + " " + self.service       

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
        return self.service    

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
        return self.interest_cate    

class Interest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    interests = models.ManyToManyField(InterestService)

    def __str__(self):
        return self.user.username
