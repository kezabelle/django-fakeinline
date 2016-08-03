# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db.models import Model

# We need this for the FakeInline
class FakeModel(Model):
    class Meta:
        managed = False
        abstract = True
