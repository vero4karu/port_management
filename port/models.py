#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vera Mazhuga http://vero4ka.info
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Ship(models.Model):
    name = models.CharField(
        max_length=36,
    )

    code = models.CharField(
        verbose_name=u'unique identifier',
        max_length=24,
        unique=True,
        validators=[RegexValidator(
            r'^[\d\w]+$',
            u'Ship identifier must be composed of letters and numbers',
        )],
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Container(models.Model):
    name = models.CharField(
        max_length=36,
    )

    ship = models.ForeignKey(
        'port.Ship',
    )

    has_dangerous_goods = models.BooleanField(
        verbose_name=u'has a fire and/or chemical hazard.',
        default=False,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Dock(models.Model):
    name = models.CharField(
        max_length=36,
    )

    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ShipInDock(models.Model):
    ship = models.ForeignKey(
        'port.Ship',
    )

    dock = models.ForeignKey(
        'port.Dock',
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    def clean(self):
        if self.ship and self.dock and self.is_active:
            if ShipInDock.objects.filter(
                    dock=self.dock,
                    is_active=True
            ).exclude(id=self.id):
                raise ValidationError('A dock can contain only one ship at a time.')

    def __unicode__(self):
        return u'{0} in {1}'.format(self.ship.name, self.dock.name)