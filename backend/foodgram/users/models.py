from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import (USER_NAME_MAX_LEN,
                        USER_EMAIL_MAX_LEN,
                        NAME_MAX_LEN,
                        LAST_NAME_MAX_LEN,
                        PASSWORD_LEN)


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        verbose_name='Логин',
        max_length=USER_NAME_MAX_LEN,
        unique=True,
        blank=False)

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=USER_EMAIL_MAX_LEN,
        unique=True
    )

    first_name = models.CharField(verbose_name='Имя',
                                  max_length=NAME_MAX_LEN,
                                  blank=False)

    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=LAST_NAME_MAX_LEN,
                                 blank=False)

    password = models.CharField(max_length=PASSWORD_LEN, verbose_name='Пароль')

    USERNAME_FIELD = ('email')

    REQUIRED_FIELDS = ('password', 'first_name', 'last_name', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
