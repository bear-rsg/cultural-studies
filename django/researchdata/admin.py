from django.contrib import admin
from . import models

admin.site.site_header = 'Cultural Studies: Admin Dashboard'
REL_INLINE_EXTRA_DEFAULT = 1
ADMIN_VIEW_LIST_PER_PAGE_DEFAULT = 50


# Inlines


class RelEntityAndEventInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Entities and Events
    """
    model = models.RelEntityAndEvent
    extra = REL_INLINE_EXTRA_DEFAULT


class RelEntityAndItemInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Entities and Items
    """
    model = models.RelEntityAndItem
    extra = REL_INLINE_EXTRA_DEFAULT


class RelEntityAndPersonInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Entities and Persons
    """
    model = models.RelEntityAndPerson
    extra = REL_INLINE_EXTRA_DEFAULT


class RelEventAndPersonInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Events and Persons
    """
    model = models.RelEventAndPerson
    extra = REL_INLINE_EXTRA_DEFAULT


class RelItemAndItemInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Items and other Items
    """
    model = models.RelItemAndItem
    extra = REL_INLINE_EXTRA_DEFAULT
    fk_name = 'item_1'


class RelItemAndPersonInline(admin.TabularInline):
    """
    A subform/inline form for relationships between Items and Persons
    """
    model = models.RelItemAndPerson
    extra = REL_INLINE_EXTRA_DEFAULT


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
        RelEntityAndPersonInline,
        RelEventAndPersonInline,
        RelItemAndPersonInline
    )
