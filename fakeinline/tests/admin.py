# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from fakeinline.datastructures import FakeInline
from fakeinline.tests.models import Model2ForTesting

class Admin2ForTesting(admin.ModelAdmin):
    inlines = [FakeInline]
admin.site.register(Model2ForTesting, Admin2ForTesting)
