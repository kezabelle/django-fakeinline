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

    # This is not required to fill out the API, but is useful for debugging ...
    def __repr__(self):
        instance = self.kwargs.get('instance', None)
        return '<%(cls)s for obj: %(parent_instance)r, using form: %(form)r>' % {
            'cls': self.__class__.__name__,
            'parent_instance': instance,
            'form': self.form,
        }

    # This is not required to fill out the API, but makes subclassing easier.
    template = "admin/edit_inline/fakeinline.html"

# class InlineChecks(InlineModelAdminChecks):
#     """ Wire up just enough to get through the system checks framework """
#     def _check_relation(self, obj, parent_model):
#         # get rid of E202, I know it doesn't have a relation to whatever the thing is
#         return []


class FakeInlineChecks(object):
    def check(self, *args, **kwargs):
        return ()

# We need to inherit from InlineModelAdmin because of E104, and because of
# https://code.djangoproject.com/ticket/26816
# its a separate subclass so that hopefully one day I can not have it...
class FakeInline(InlineModelAdmin):
    # model must be not None, and a subclass of Model, because of E105
    # raised by the *parent* modeladmin in ModelAdminChecks._check_inlines_item
    model = FakeModel
    checks_class = FakeInlineChecks
    min_num = 1
    max_num = 1
    # This is necessary to avoid needing to subclass BaseModelFormSet
    # because of the system check.
    formset = FakeFormSet

    @property
    def template(self):
        return self.formset.template

    def get_formset(self, request, obj=None, **kwargs):
        # We're constructing a dynamic (unpicklable, sorry!) subclass
        # and attaching all the admin data to it, so that the formset
        # instance may do stuff.
        formset = self.formset
        parent_type = formset.__name__
        clsname = str('AdminAware%s' % parent_type)
        extra_attrs = {
            'admin_site': self.admin_site,
            'parent_modeladmin': self.admin_site._registry[self.parent_model],
            'request': request,
            'instance': obj,
        }
        cls = type(clsname, (formset,), extra_attrs)
        return cls

    def get_queryset(self, *args, **kwargs):
        return () # QuerySet(model=self.model).none() causes issues.

    # This is not required to fill out the API, but is useful for debugging ...
    def __repr__(self):
        return '<%(cls)s using formset: %(formset)r>' % {
            'cls': self.__class__.__name__,
            'formset': FakeFormSet,
        }
