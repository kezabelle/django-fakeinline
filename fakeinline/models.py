# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db.models import Model

class FakeModel(Model):
    class Meta:
        managed = False