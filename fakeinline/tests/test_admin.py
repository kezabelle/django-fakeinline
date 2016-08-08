# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

try:
    from urllib.parse import urlparse
except ImportError:  # py2.7 ... just for 1.8 tbh.
    from urlparse import urlparse
import pytest
from django.contrib import admin
from django.core.urlresolvers import reverse
from fakeinline.datastructures import FakeInline
from .models import ModelForTesting

class AdminForTesting(admin.ModelAdmin):
    inlines = [FakeInline]


@pytest.yield_fixture
def django_admin():
    admin.site.register(ModelForTesting, AdminForTesting)
    yield admin.site._registry[ModelForTesting]
    admin.site.unregister(ModelForTesting)


def test_not_there():
    assert ModelForTesting not in admin.site._registry


def test_GET_ok(django_admin, admin_client):
    url = reverse('admin:tests_modelfortesting_add')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_POST_ok(django_admin, admin_client):
    url = reverse('admin:tests_modelfortesting_add')
    redirect_to = reverse('admin:tests_modelfortesting_changelist')
    response = admin_client.post(url, data={}, follow=True)
    assert response.status_code == 200
    # 1.8 included the http://host so we have to parse it out for compatibility.
    # 1.9+ doesn't.
    redirects = [(urlparse(url).path, code) for url, code in response.redirect_chain]
    assert redirects == [(urlparse(redirect_to).path, 302)]
