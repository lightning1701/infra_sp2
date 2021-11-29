import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class UserManager(UserManager):

    def create_user(self, username, email,
                    password=None, role='user',
                    bio=None):
        """
        Создаем кастом-пользователя
        """
        if not email:
            raise ValueError('Емейл обязателен для регистрации')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=uuid.uuid4(),
            role=role,
            bio=bio
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,
                         email, password=None,
                         role=None, bio=None):
        """
        Создаем супер-пользователя
        """
        user = self.create_user(username, email, bio)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.role = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Класс кастом пользователя с доп. полями
    """

    objects = UserManager()
    ADMIN_ROLE = 'admin'
    MODERATOR_ROLE = 'moderator'
    USER_ROLE = 'user'
    all_roles = [
        (ADMIN_ROLE, 'Администратор'),
        (MODERATOR_ROLE, 'Модератор'),
        (USER_ROLE, 'Пользователь')
    ]
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=all_roles,
        default=USER_ROLE
    )
    email = models.EmailField(
        verbose_name='Email адрес',
        max_length=255,
        unique=True,
    )
    confirmation_code = models.CharField(
        verbose_name='Код доступа', max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return (
            f'{self.username} - username; {self.role} - роль;'
            f'{self.confirmation_code} - код доступа;'
            f'{self.is_superuser}')

    def is_admin(self):
        """
        Пользователь администратор?
        """
        return self.role == self.ADMIN_ROLE

    def is_moderator(self):
        """
        Пользователь модератор?
        """
        return self.role == self.MODERATOR_ROLE
