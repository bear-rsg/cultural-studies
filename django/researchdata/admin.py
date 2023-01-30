from django.contrib import admin
from django.contrib.auth.models import Group
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
    list_display = ('first_name',)
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
    inlines = (
        PersonHistoryInline,
        RelEntityAndPersonInline,
        RelEventAndPersonInline,
        RelItemAndPersonInline
    )
