# -*- coding: utf-8 -*-
from __future__ import absolute_import,  unicode_literals

import pytest
from django.contrib import admin
from fakeinline.datastructures import FakeInline
from fakeinline.tests.models import ModelForTesting
from fakeinline.tests.test_admin import AdminForTesting


@pytest.yield_fixture
def django_admin():
    admin.site.register(ModelForTesting, AdminForTesting)
    yield admin.site._registry[ModelForTesting]
    admin.site.unregister(ModelForTesting)

def test_self_binding_on_dynamic_formset(rf, django_admin):
    """
    Because class attrs and doing self.x.append(1) in a ModelAdmin are
    prone to problems, lets do some quick sanity checking here and hope for
    the best, yeah?
    """
    inline = FakeInline(parent_model=ModelForTesting, admin_site=admin.site)
    request = rf.get('/')
    formset = inline.get_formset(request, obj=None)()
    assert formset.admin_site is admin.site
    assert formset.parent_modeladmin is django_admin
    assert formset.request is request
    assert formset.instance is None
    formset2 = inline.get_formset(request, obj=None)()
    # now we do some rebinding of `formset` attrs and make sure they don't
    # copy to `formset2` because class attrs.
    # we make all of them mutable and then append stuff to them to hopefully
    # make more sure.
    formset.admin_site = [1]
    formset.parent_modeladmin = [2]
    formset.request = [3]
    formset.instance = [4]
    formset.admin_site.append(100)
    formset.parent_modeladmin.append(100)
    formset.request.append(100)
    formset.instance.append(100)
    assert formset2.admin_site != [1, 100]
    assert formset2.parent_modeladmin != [2, 100]
    assert formset2.request != [3, 100]
    assert formset2.instance != [4, 100]
    # we should still have the same attrs as `formset` originally had
    assert formset2.admin_site is admin.site
    assert formset2.parent_modeladmin is django_admin
    assert formset2.request is request
    assert formset2.instance is None
    # having changed `formset`, make sure subsequent generations afterwards
    # also don't have the problem, yeah?
    formset3 = inline.get_formset(request, obj=None)()
    # check this version also has the right original attrs as per `formset`
    assert formset3.admin_site is admin.site
    assert formset3.parent_modeladmin is django_admin
    assert formset3.request is request
    assert formset3.instance is None
