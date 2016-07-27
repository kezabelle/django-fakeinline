# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from fakeinline.datastructures import FakeInline
from .models import TestModel

class TestAdmin(admin.ModelAdmin):
    inlines = [FakeInline]
admin.site.register(TestModel, TestAdmin)
