from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.utils.html import mark_safe
from . import models


admin.site.site_header = 'Cultural Studies: Admin Dashboard'
admin.site.unregister(Group)
INLINE_EXTRA_DEFAULT = 1
ADMIN_VIEW_LIST_PER_PAGE_DEFAULT = 50


# Inlines


class PersonHistoryInline(admin.StackedInline):
    """
    A subform/inline form for PersonHistory, to be used in the PersonAdminView
    """
    model = models.PersonHistory
    extra = INLINE_EXTRA_DEFAULT


class RelEntityAndEventInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Entities and Events
    """
    model = models.RelEntityAndEvent
    extra = INLINE_EXTRA_DEFAULT


class RelEntityAndItemInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Entities and Items
    """
    model = models.RelEntityAndItem
    extra = INLINE_EXTRA_DEFAULT


class RelEntityAndPersonInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Entities and Persons
    """
    model = models.RelEntityAndPerson
    extra = INLINE_EXTRA_DEFAULT


class RelEventAndPersonInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Events and Persons
    """
    model = models.RelEventAndPerson
    extra = INLINE_EXTRA_DEFAULT


class RelItemAndItemInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Items and other Items
    """
    model = models.RelItemAndItem
    extra = INLINE_EXTRA_DEFAULT
    fk_name = 'item_1'


class RelItemAndPersonInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Items and Persons
    """
    model = models.RelItemAndPerson
    extra = INLINE_EXTRA_DEFAULT


# AdminViews


@admin.register(models.Entity)
class EntityAdminView(admin.ModelAdmin):
    """
    Customise the Entity section of the admin dashboard
    """
    list_display = ('name',)
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
    inlines = (
        RelEntityAndEventInline,
        RelEntityAndItemInline,
        RelEntityAndPersonInline
    )


@admin.register(models.Event)
class EventAdminView(admin.ModelAdmin):
    """
    Customise the Event section of the admin dashboard
    """
    list_display = ('name',)
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
    inlines = (
        RelEntityAndEventInline,
        RelEventAndPersonInline
    )


@admin.register(models.Item)
class ItemAdminView(admin.ModelAdmin):
    """
    Customise the Item section of the Django admin
    """
    list_display = ('name',)
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
    inlines = (
        RelEntityAndItemInline,
        RelItemAndItemInline,
        RelItemAndPersonInline
    )


@admin.register(models.Person)
class PersonAdminView(admin.ModelAdmin):
    """
    Customise the Person section of the admin dashboard
    """
    list_display = ('first_name', 'use_as_template')
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
    inlines = (
        PersonHistoryInline,
        RelEntityAndPersonInline,
        RelEventAndPersonInline,
        RelItemAndPersonInline
    )

    def use_as_template(self, obj):
        return mark_safe(f'<a href="/dashboard/researchdata/person/add/?obj_id={obj.id}">Use as Template</a>')
    use_as_template.short_description = 'Use as Template'

    def add_view(self, request, form_url='', extra_context=None):
        """
        To allow for existing objects to be used as 'templates'
        i.e. pre-filled form fields on new object form.
        If the 'obj_id' parameter is provided in URL
        e.g. ".../add/?obj_id=1" will prefill a new obj form with data from person object
        """

        # If 'obj_id' is a provided parameter, add the object's data to the request
        obj_id = request.GET.get('obj_id', None)
        if obj_id is not None:
            g = request.GET.copy()
            g.update(model_to_dict(models.Person.objects.get(id=obj_id)))
            request.GET = g

        return super().add_view(request, form_url, extra_context)
