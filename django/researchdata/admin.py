from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import ManyToManyField, ForeignKey
from django.forms.models import model_to_dict
from django.utils.html import mark_safe
from django.urls import reverse
from . import models


admin.site.site_header = 'Cultural Studies: Admin Dashboard'
admin.site.unregister(Group)

CUSTOM_ADMIN_CSS = {'all': ('/static/css/admin.css',)}
INLINE_EXTRA_DEFAULT = 1
ADMIN_VIEW_LIST_PER_PAGE_DEFAULT = 50
RELATIONSHIP_STANDARD_FIELDS = [
    'type',
    ('relationship_start_date_year', 'relationship_start_date_month', 'relationship_start_date_day'),
    ('relationship_start_year_range_from', 'relationship_start_year_range_to', 'relationship_start_date_details'),
    ('relationship_end_date_year', 'relationship_end_date_month', 'relationship_end_date_day'),
    ('relationship_end_year_range_from', 'relationship_end_year_range_to', 'relationship_end_date_details'),
    'relationship_details'
]


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ManyToManyField and f.name not in exclude)


def get_fk_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of ForeignKey fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ForeignKey and f.name not in exclude)


# Generic Classes (to be inherited below)


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


class GenericStackedInlineAdminView(admin.StackedInline):
    """
    This is a generic base class that can be inherited from by StackedInline admin views
    """
    extra = INLINE_EXTRA_DEFAULT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all FK fields to be autocomplete_fields (i.e. searchable select lists)
        self.autocomplete_fields = get_fk_fields(self.model)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all FK fields to be autocomplete_fields (i.e. searchable select lists)
        self.autocomplete_fields = get_fk_fields(self.model)

    class Media:
        css = CUSTOM_ADMIN_CSS


# Inlines


class EntityHistoryInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for EntityHistory, to be used in the EntityAdminView
    """
    model = models.EntityHistory
    extra = INLINE_EXTRA_DEFAULT
    fk_name = 'entity'
    fields = (
        'entity',
        'name',
        ('start_date_year', 'start_date_month', 'start_date_day'),
        ('start_year_range_from', 'start_year_range_to', 'start_date_details'),
        ('end_date_year', 'end_date_month', 'end_date_day'),
        ('end_year_range_from', 'end_year_range_to', 'end_date_details'),
    )


class PersonHistoryInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for PersonHistory, to be used in the PersonAdminView
    """
    model = models.PersonHistory
    fields = (
        'person',
        ('first_name', 'last_name'),
        'other_names',
        ('start_date_year', 'start_date_month', 'start_date_day'),
        ('start_year_range_from', 'start_year_range_to', 'start_date_details'),
        ('end_date_year', 'end_date_month', 'end_date_day'),
        ('end_year_range_from', 'end_year_range_to', 'end_date_details'),
    )


class RelEntityAndEntityInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Entities and other Entities
    """
    model = models.RelEntityAndEntity
    fk_name = 'entity_1'
    fields = [
        'entity_1',
        'entity_2',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelEntityAndEventInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Entities and Events
    """
    model = models.RelEntityAndEvent
    fields = [
        'entity',
        'event',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelEntityAndItemInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Entities and Items
    """
    model = models.RelEntityAndItem
    fields = [
        'entity',
        'item',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelEntityAndPersonInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Entities and Persons
    """
    model = models.RelEntityAndPerson
    fields = [
        'entity',
        'person',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelEventAndItemInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Events and Items
    """
    model = models.RelEventAndItem
    fields = [
        'event',
        'item',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelEventAndPersonInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Events and Persons
    """
    model = models.RelEventAndPerson
    fields = [
        'event',
        'person',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelItemAndItemInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Items and other Items
    """
    model = models.RelItemAndItem
    fk_name = 'item_1'
    fields = [
        'item_1',
        'item_2',
    ] + RELATIONSHIP_STANDARD_FIELDS


class RelItemAndPersonInline(GenericStackedInlineAdminView):
    """
    A subform/inline form for relationships between Items and Persons
    """
    model = models.RelItemAndPerson
    fields = [
        'item',
        'person',
    ] + RELATIONSHIP_STANDARD_FIELDS


# AdminViews


@admin.register(models.Entity)
class EntityAdminView(GenericAdminView):
    """
    Customise the Entity section of the admin dashboard
    """
    list_display = ('name', 'use_as_template')
    inlines = (
        EntityHistoryInline,
        RelEntityAndEntityInline,
        RelEntityAndEventInline,
        RelEntityAndItemInline,
        RelEntityAndPersonInline
    )
    search_fields = (
        'name',
        'type__name',
        'admin_notes'
    )
    fieldsets = (
        ('Entity', {
            'fields': (
                'name',
                'type',
                ('date_year', 'date_month', 'date_day'),
                ('year_range_from', 'year_range_to', 'date_details'),
                'admin_notes',
            ),
        }),
    )


@admin.register(models.Event)
class EventAdminView(GenericAdminView):
    """
    Customise the Event section of the admin dashboard
    """
    list_display = ('name', 'location', 'start', 'end', 'use_as_template')
    inlines = (
        RelEntityAndEventInline,
        RelEventAndItemInline,
        RelEventAndPersonInline
    )
    search_fields = (
        'name',
        'type__name',
        'activity__name',
        'language__name',
        'frequency__name',
        'location',
        'admin_notes'
    )
    fieldsets = (
        ('Entity', {
            'fields': (
                'name',
                'type',
                'activity',
                'language',
                'frequency',
                ('location', 'location_coordinates',)
            )
        }),
        ('Start Date/Time', {
            'fields': (
                ('start_date_year', 'start_date_month', 'start_date_day'),
                ('start_year_range_from', 'start_year_range_to'),
                ('start_time', 'start_date_time_details'),
            ),
        }),
        ('End Date/Time', {
            'fields': (
                ('end_date_year', 'end_date_month', 'end_date_day'),
                ('end_year_range_from', 'end_year_range_to'),
                ('end_time', 'end_date_time_details'),
            ),
        }),
        ('Admin', {
            'fields': (
                'admin_notes',
            ),
        })
    )


@admin.register(models.Item)
class ItemAdminView(GenericAdminView):
    """
    Customise the Item section of the Django admin
    """
    list_display = ('name', 'item_id', 'finding_aid', 'is_a_collective_item', 'publication_status', 'use_as_template')
    inlines = (
        RelEntityAndItemInline,
        RelEventAndItemInline,
        RelItemAndItemInline,
        RelItemAndPersonInline
    )
    search_fields = (
        'name',
        'item_id',
        'finding_aid',
        'is_a_collective_item',
        'type__name',
        'media__name',
        'language__name',
        'publication_status__name',
        'description',
        'digital_materials_url',
        'admin_notes'
    )
    fieldsets = (
        ('Item', {
            'fields': (
                'name',
                'item_id',
                'finding_aid',
                'is_a_collective_item',
                'type',
                'media',
                'language',
                'publication_status',
                'description',
            )
        }),
        ('Created Date', {
            'fields': (
                ('created_date_year', 'created_date_month', 'created_date_day'),
                ('created_year_range_from', 'created_year_range_to', 'created_date_details'),
            ),
        }),
        ('Admin', {
            'fields': (
                'admin_notes',
            ),
        })
    )


@admin.register(models.Person)
class PersonAdminView(GenericAdminView):
    """
    Customise the Person section of the admin dashboard
    """
    list_display = ('first_name',
                    'last_name',
                    'other_names',
                    'is_a_group_of_persons',
                    'group_of_persons_description',
                    'use_as_template')
    inlines = (
        PersonHistoryInline,
        RelEntityAndPersonInline,
        RelEventAndPersonInline,
        RelItemAndPersonInline
    )
    search_fields = (
        'title',
        'first_name',
        'last_name',
        'other_names',
        'group_of_persons_description',
        'admin_notes'
    )
    fieldsets = (
        ('Person', {
            'fields': (
                'title',
                ('first_name', 'last_name'),
                'other_names',
                ('is_a_group_of_persons', 'group_of_persons_description'),
            )
        }),
        ('Birth Date', {
            'fields': (
                ('birth_date_year', 'birth_date_month', 'birth_date_day'),
                ('birth_year_range_from', 'birth_year_range_to', 'birth_date_details')
            ),
        }),
        ('Death Date', {
            'fields': (
                ('death_date_year', 'death_date_month', 'death_date_day'),
                ('death_year_range_from', 'death_year_range_to', 'death_date_details')
            ),
        }),
        ('Admin', {
            'fields': (
                'admin_notes',
            ),
        })
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
admin.site.register(models.SlTypeRelEntityAndEntity, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndEvent, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelEntityAndPerson, GenericSlAdminView)
admin.site.register(models.SlTypeRelEventAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelEventAndPerson, GenericSlAdminView)
admin.site.register(models.SlTypeRelItemAndItem, GenericSlAdminView)
admin.site.register(models.SlTypeRelItemAndPerson, GenericSlAdminView)
