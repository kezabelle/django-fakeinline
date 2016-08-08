django-fakeinline
=================

:author: Keryn Knight
:version: 0.1.1

``fakeinline`` provides enough of the methods and attributes to trick the
`Django Admin`_ into displaying it when mounted as part of an ``inlines``
declaration on a ModelAdmin. Where possible it does so without subclassing
real Django classes, as should be the case with `Duck Typing`_.

The 2 necessary subclasses are the ``FakeInline`` class itself, which must
subclass ``InlineModelAdmin``, and the ``model`` attribute, ``FakeModel`` which
must subclass ``Model``, but is unmanaged and abstract, so there is nothing
touching the database.

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-fakeinline.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-fakeinline

==============  ======
Release         Status
==============  ======
master          |travis_master|
==============  ======

Why?!
-----

The most interesting thing about the `Django Admin`_ is trying to bend it to
my will. This is an example of my winning.

No really, why?
---------------

Because it's actually nicer to be able to wedge additional things into the admin,
without overriding the ``change_form.html`` template on a per-model, per-app basis.

Example usage
-------------

Here's a simple way of putting the classic words **Hello world** onto a ModelAdmin::

    class MyFormset(FakeFormset):
        # this probably works, but usually you'd point it at a template file.
        template = Template('{{inline_admin_formset.formset.get_data}}')

        def get_data(self, *a, **kw):
            return 'Hello world'

    class MyInline(FakeInline):
        formset = MyFormSet

    class MyAdmin(ModelAdmin):
        inlines = [MyInline]

Whilst a silly example, it demonstrates how one might encapsulate display data
(charts, change history, etc) in a re-usable(ish) component for display on the
change view.

Tests
-----

There's a couple in ``fakeinline.tests`` ... just enough to verify it doesn't
raise an exception on GET or POST.

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
.. _Django Admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
.. _Duck Typing: https://en.wikipedia.org/wiki/Duck_typing
