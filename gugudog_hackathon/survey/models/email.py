from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

try:
    from django.conf import settings

    if settings.AUTH_USER_MODEL:
        user_model = settings.AUTH_USER_MODEL
    else:
        user_model = User
except (ImportError, AttributeError):
    user_model = User

class Email(models.Model):

    email = models.CharField(max_length=500)
    # EmailField도 있으나 우선 제출을 많이 받고 나중에 걸러내도 되기에 CharField 사용했습니다.
    # EmailField로 바꿔도 괜찮음

    user = models.ForeignKey(
        user_model,
        on_delete=models.SET_NULL,
        verbose_name=_("User"),
        null=True,
        blank=True,
        related_name="email_of_user"
    )

    def __str__(self):
        return self.email

    class Meta(object):
        verbose_name = _("Emails Submitted by Users")
        verbose_name_plural = _("Emails Submitted by Users") 