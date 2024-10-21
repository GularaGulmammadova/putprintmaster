from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(username=username,
                          email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(username, email, password, **extra_fields)
        return user

    def deactivate_user(self, user_id):
        try:
            user = self.get(pk=user_id)
        except self.model.DoesNotExist:
            raise ValueError(
                "User with ID: {user_id} not found".format(user_id))

        user.is_active = False
        user.save(using=self._db)
        return user


