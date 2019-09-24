from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

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
    description_detail = models.TextField(null=True, blank=True)

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
    count_gudog_users = property(get_gudog_users)

    # 서비스를 찜한 유저의 수
    # @property

    def get_zzim_users(self):
        return self.zzim_users.all().count()

    count_zzim_users = property(get_zzim_users)

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

    # 결제까지 남은 일수를 구하기 위한 코드
    def get_remained_date(self):
        pay_after = self.register_date.day - timezone.now().day
        
        date_format = "%m"
        # print(pay_after)
        # pay_after = int(str(pay_after).split(' ')[0])
        if pay_after < 0:
            # 음수면 구독시작일의 월 + 1하고 현재 날짜를 뺀 날의 day를 참조한다.
            now = datetime.now()
            month = now.timetuple().tm_mon
            month += 1
            now = now.replace(month=month)
            now = now.replace(day=self.register_date.day)
            # print(now)
            # pay_after = now - timezone.now()
            # print(now, " - ", datetime.now(), " = ", now-datetime.now())
            pay_after = now - datetime.now()
            pay_after = pay_after.days
            pay_after = str(pay_after) + "일 후 결제됩니다."
            # pay_after = int(str(now - datetime.now()).split(' ')[0])

        elif pay_after == 0:
            pay_after = "오늘 결제됩니다."
        else:
            pay_after = str(pay_after) + "일 후 결제됩니다."
        # print(pay_after, "일 후 결제됩니다.")
        # print(self.register_date)
        return pay_after
    
    # 구독한 날짜(일) 순 정렬을 위한 _remained_date 코드
    def _remained_date(self):
        today = timezone.now().day
        sub_date = self.register_date.day - today
        if sub_date < 0:
            sub_date += 100
        return sub_date
    remained_date = property(_remained_date)

    def __str__(self):
        return str(self.user) + " " + str(self.service)       

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
        return str(self.user) + " " + str(self.service)    

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