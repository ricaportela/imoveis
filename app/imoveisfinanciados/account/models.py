# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.shortcuts import resolve_url as r
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_(u"O email é obrigatório."))
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password, **extra_fields):
        u = self.create_user(email, first_name, last_name, phone, password, **extra_fields)
        u.is_admin = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'),
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        _("Nome"),
        max_length=255,
    )
    last_name = models.CharField(
        _("Sobrenome"),
        max_length=255,
    )
    phone = models.CharField(
        _(u"Telefone"),
        max_length=15,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            _('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    )
    is_admin = models.BooleanField(
        _('admin'),
        default=False,
        help_text=_(u"Indica que o usuário pode acessar o painel administrativo."),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def get_absolute_url(self):
        return r("/users/%s/" % (self.username))

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
