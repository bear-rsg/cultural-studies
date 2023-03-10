from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.utils.html import mark_safe
from django.urls import reverse
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


class EntityHistoryInline(admin.StackedInline):
    """
    A subform/inline form for EntityHistory, to be used in the EntityAdminView
    """
    model = models.EntityHistory
    extra = INLINE_EXTRA_DEFAULT
    fk_name = 'entity'


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


class RelEventAndItemInline(admin.StackedInline):
    """
    A subform/inline form for relationships between Events and Items
    """
    model = models.RelEventAndItem
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


class GenericSlAdminView(admin.ModelAdmin):
    """
    This is a generic base class that can be inherited from by Select List models

    This class can either be inherited from if further customisations are needed, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if no changes are needed, just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('name',)

    def get_model_perms(self, request):
        """
        Hide SL tables from admin side bar, but still CRUD via inline shortcuts on main models
        """
        return {}


class GenericAdminView(admin.ModelAdmin):
    """
    A generic admin view to be inherited and extended by specific admin views below
    """
    list_display = ('id', 'use_as_template',)
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT

    def use_as_template(self, obj):
        add_form_url = reverse(f'admin:researchdata_{self.model._meta.model_name}_add')
        return mark_safe(f'<a href="{add_form_url}?obj_id={obj.id}">Use as Template</a>')
    use_as_template.short_description = 'Use as Template'

    def add_view(self, request, form_url='', extra_context=None):
        """
        To allow for existing objects to be used as 'templates'
        i.e. pre-filled form fields on new object form.
        If the 'obj_id' parameter is provided in URL
        e.g. ".../add/?obj_id=1" will prefill a new obj form with data from an existing object
        """

        # If 'obj_id' is a provided parameter, add the object's data to the request
        obj_id = request.GET.get('obj_id', None)
        if obj_id is not None:
            g = request.GET.copy()
            g.update(model_to_dict(self.model.objects.get(id=obj_id)))
            request.GET = g

        return super().add_view(request, form_url, extra_context)


@admin.register(models.Entity)
class EntityAdminView(GenericAdminView):
    """
    Customise the Entity section of the admin dashboard
    """
    list_display = ('name', 'use_as_template')
    inlines = (
        EntityHistoryInline,
        RelEntityAndEventInline,
        RelEntityAndItemInline,
        RelEntityAndPersonInline
    )


@admin.register(models.Event)
class EventAdminView(GenericAdminView):
    """
    Customise the Event section of the admin dashboard
    """
    list_display = ('name', 'use_as_template')
    inlines = (
        RelEntityAndEventInline,
        RelEventAndItemInline,
        RelEventAndPersonInline
    )


@admin.register(models.Item)
class ItemAdminView(GenericAdminView):
    """
    Customise the Item section of the Django admin
    """
    list_display = ('name', 'use_as_template')
    inlines = (
        RelEntityAndItemInline,
        RelEventAndItemInline,
        RelItemAndItemInline,
        RelItemAndPersonInline
    )


@admin.register(models.Person)
class PersonAdminView(GenericAdminView):
    """
    Customise the Person section of the admin dashboard
    """
    list_display = ('first_name', 'use_as_template')
    inlines = (
        PersonHistoryInline,
        RelEntityAndPersonInline,
        RelEventAndPersonInline,
        RelItemAndPersonInline
    )


# Register SL Admin Views
admin.site.register(models.SlEntityType, GenericSlAdminView)
admin.site.register(models.SlEventActivity, GenericSlAdminView)
admin.site.register(models.SlEventFrequency, GenericSlAdminView)
admin.site.register(models.SlEventType, GenericSlAdminView)
admin.site.register(models.SlItemFindingAid, GenericSlAdminView)
admin.site.register(models.SlItemMedia, GenericSlAdminView)
admin.site.register(models.SlItemPublicationStatus, GenericSlAdminView)
admin.site.register(models.SlItemType, GenericSlAdminView)
admin.site.register(models.SlLanguage, GenericSlAdminView)
admin.site.register(models.SlPersonTitle, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndEvent, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndPerson, GenericSlAdminView)
admin.site.register(models.SlTypeRelEventAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelEventAndPerson, GenericSlAdminView)
admin.site.register(models.SlTypeRelItemAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelItemAndPerson, GenericSlAdminView)
