# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db.models import Model

class ModelForTesting(Model):
    class Meta:
        app_label = 'tests'


class Model2ForTesting(Model):
    class Meta:
        app_label = 'tests'
