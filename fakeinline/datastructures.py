# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.forms import Media
from django.contrib.admin.checks import InlineModelAdminChecks
from django.contrib.admin.options import InlineModelAdmin
from .models import FakeModel

class FakeForm(object):
    """ Enough of the Form API to fool Django. """
    # The following attributes and methods are defined in the order
    # they caused me an error when trying to load or POST the view.
    base_fields = []
    media = Media()


class FakeFormSet(object):
    """ Enough of the FormSet API to fool Django. """
    # The following attributes and methods are defined in the order
    # they caused me an error when trying to load or POST the view.
    @classmethod
    def get_default_prefix(cls):
        return 'edit_region_chunk_formset'

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    form = FakeForm
    media = Media()
    initial_forms = ()

    def get_queryset(self):
        return ()

    extra_forms = ()
    empty_form = FakeForm

    def is_valid(self, *args, **kwargs):
        return True

    def save(self, *args, **kwargs):
        return True

    new_objects = ()
    changed_objects = ()
    deleted_objects = ()

    def non_form_errors(self, *args, **kwargs):
        return ()

    errors = ()

class InlineChecks(InlineModelAdminChecks):
    """ Wire up just enough to get through the system checks framework """
    def _check_relation(self, obj, parent_model):
        # Go away I know it doesn't have a relation to whatever the thing is
        return []

# We need to inherit from InlineModelAdmin and set this because of
# https://code.djangoproject.com/ticket/26816
# its a separate subclass so that hopefully one day I can not have it...
class FakeInline(InlineModelAdmin):
    model = FakeModel
    checks_class = InlineChecks
    template = "admin/edit_inline/fakeinline.html"
    def get_formset(self, request, obj=None, **kwargs):
        return FakeFormSet
