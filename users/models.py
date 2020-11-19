from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoleChoices(models.TextChoices):
    """
    Константы пользовательских ролей.
    """
    USER = ('user', 'пользователь',)
    MODERATOR = ('moderator', 'модератор',)
    ADMIN = ('admin', 'администратор',)


class User(AbstractUser):
    """
    Расширение пользовательской модели (User).
    """

    role = models.CharField(verbose_name='роль пользователя',
                            choices=UserRoleChoices.choices,
                            default=UserRoleChoices.USER,
                            max_length=50)
    bio = models.TextField(verbose_name='биография', null=True, blank=True)

    @property
    def is_moderator(self) -> bool:
        """
        Проверка наличия статуса модератора.
        """
        return self.role == UserRoleChoices.MODERATOR

    @property
    def is_admin(self) -> bool:
        """
        Проверка наличия статуса администратора или статуса
        суперпользователя, который равен администратору.
        """
        return self.role == UserRoleChoices.ADMIN or self.is_staff

    class Meta:
        ordering = ['id']
