from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def save(self, *args, **kwargs):
    #     self.set_password(raw_password=self.password)
    #     super().save(*args, **kwargs)


