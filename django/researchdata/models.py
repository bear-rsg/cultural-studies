from django.db import models
from django.db.models.functions import Upper
from location_field.models.plain import PlainLocationField
from django.core.validators import MaxValueValidator, MinValueValidator


# Select List tables


class SlAbstract(models.Model):
    """
    An abstract model for Select List models
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


class SlEntityType(SlAbstract):
    """
    Select List model used by Entity model (inherits from SlAbstract model)
    The type/category of an entity. E.g. publisher, university, department, centre
    """


class SlEventActivity(SlAbstract):
    """
    Select List model used by Event model (inherits from SlAbstract model)
    The activity that's being carried out at the event. E.g. publishing, writing, speaking
    """


class SlEventFrequency(SlAbstract):
    """
    Select List model used by Event model (inherits from SlAbstract model)
    The frequency that the event repeats. E.g. weekly, monthly, annually
    """


class SlEventType(SlAbstract):
    """
    Select List model used by Event model (inherits from SlAbstract model)
    The type/category of an event. E.g. conference, seminar, meeting
    """


class SlItemFindingAid(SlAbstract):
    """
    Select List model used by Item model (inherits from SlAbstract model)
    A document containing research findings, from which Items are obtained
    """


class SlItemMedia(SlAbstract):
    """
    Select List model used by Item model (inherits from SlAbstract model)
    The type of media of an item. E.g. print, video
    """


class SlItemPublicationStatus(SlAbstract):
    """
    Select List model used by Item model (inherits from SlAbstract model)
    The publication status of an item. E.g. published, unpublished
    """


class SlItemType(SlAbstract):
    """
    Select List model used by Item model (inherits from SlAbstract model)
    The type/category of an item. E.g. minutes, memo, teaching materials
    """


class SlLanguage(SlAbstract):
    """
    Select List model used by various models (inherits from SlAbstract model)
    A language. E.g. English, French, German
    """


class SlPersonTitle(SlAbstract):
    """
    Select List model used by Person model (inherits from SlAbstract model)
    A title of a person, e.g. Mrs, Ms, Miss, Dr, Mr, etc.
    """


class SlTypeRelEntityAndEvent(SlAbstract):
    """
    Select List model used by RelEntityAndEvent (inherits from SlAbstract model)
    A type of relationship between Entity and Event
    """


class SlTypeRelEntityAndItem(SlAbstract):
    """
    Select List model used by RelEntityAndItem (inherits from SlAbstract model)
    A type of relationship between Entity and Item
    """


class SlTypeRelEntityAndPerson(SlAbstract):
    """
    Select List model used by RelEntityAndPerson (inherits from SlAbstract model)
    A type of relationship between Entity and Person
    """


class SlTypeRelEventAndItem(SlAbstract):
    """
    Select List model used by RelEventAndItem (inherits from SlAbstract model)
    A type of relationship between Event and Item
    """


class SlTypeRelEventAndPerson(SlAbstract):
    """
    Select List model used by RelEventAndPerson (inherits from SlAbstract model)
    A type of relationship between Event and Person
    """


class SlTypeRelItemAndItem(SlAbstract):
    """
    Select List model used by RelItemAndItem (inherits from SlAbstract model)
    A type of relationship between Item and Item
    """


class SlTypeRelItemAndPerson(SlAbstract):
    """
    Select List model used by RelItemAndPerson (inherits from SlAbstract model)
    A type of relationship between Item and Person
    """


# Main tables


class Entity(models.Model):
    """
    A collection of people, such as an organisation (e.g. a publisher, a University, etc)
    or a division/department/centre within an organisation or a seminar/working group
    """

    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(SlEntityType, on_delete=models.SET_NULL, blank=True, null=True)
    parent_entity = models.ForeignKey('Entity', on_delete=models.CASCADE, blank=True, null=True)
    date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='date (year)'
    )
    date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='date (month)'
    )
    date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='date (day)'
    )
    date_details = models.CharField(max_length=1000, blank=True, null=True)

    # Admin and meta fields
    admin_notes = models.TextField(blank=True, null=True)
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'entities'


class EntityHistory(models.Model):
    """
    Historical changes to a Entity object, e.g. previous names, types, etc.
    """

    entity = models.ForeignKey(Entity,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='entity_history')
    name = models.CharField(max_length=255, unique=True)

    # Change start date
    start_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='start date (year)'
    )
    start_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='start date (month)'
    )
    start_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='start date (day)'
    )
    start_date_details = models.CharField(max_length=1000, blank=True, null=True)

    # Change end date
    end_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='end date (year)'
    )
    end_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='end date (month)'
    )
    end_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='end date (day)'
    )
    end_date_details = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'entity histories'


class Event(models.Model):
    """
    A meeting, conference, seminar, etc.
    """

    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(SlEventType, on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(SlEventActivity, on_delete=models.SET_NULL, blank=True, null=True)
    language = models.ForeignKey(SlLanguage, on_delete=models.SET_NULL, blank=True, null=True)
    frequency = models.ForeignKey(SlEventFrequency, on_delete=models.SET_NULL, blank=True, null=True)

    # Location
    location = models.CharField(max_length=255,
                                blank=True,
                                null=True,
                                verbose_name='location (search)')
    location_coordinates = PlainLocationField(based_fields=['location'],
                                              zoom=7,
                                              blank=True,
                                              null=True,
                                              verbose_name='location (coordinates)')

    # Start date/time
    start_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='start date (year)'
    )
    start_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='start date (month)'
    )
    start_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='start date (day)'
    )
    start_time = models.TimeField(blank=True, null=True)
    start_date_time_details = models.CharField(max_length=1000, blank=True, null=True)

    # End date/time
    end_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='end date (year)'
    )
    end_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='end date (month)'
    )
    end_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='end date (day)'
    )
    end_time = models.TimeField(blank=True, null=True)
    end_date_time_details = models.CharField(max_length=1000, blank=True, null=True)

    # Admin and meta fields
    admin_notes = models.TextField(blank=True, null=True)
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    An object/document within a collection
    """

    name = models.CharField(max_length=255, unique=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    finding_aid = models.ForeignKey(SlItemFindingAid, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.ForeignKey(SlItemType, on_delete=models.SET_NULL, blank=True, null=True)
    media = models.ForeignKey(SlItemMedia, on_delete=models.SET_NULL, blank=True, null=True)
    language = models.ForeignKey(SlLanguage, on_delete=models.SET_NULL, blank=True, null=True)
    publication_status = models.ForeignKey(SlItemPublicationStatus, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sponsorship = models.TextField(blank=True, null=True)
    created_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='created date (year)'
    )
    created_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='created date (month)'
    )
    created_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='created date (day)'
    )
    created_date_details = models.CharField(max_length=1000, blank=True, null=True)

    # Admin and meta fields
    admin_notes = models.TextField(blank=True, null=True)
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    def __str__(self):
        return self.name


class Person(models.Model):
    """
    A person that's associated with other data, e.g. an author of an Item
    """

    title = models.ForeignKey(SlPersonTitle, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    other_names = models.CharField(max_length=255, blank=True, null=True)

    # Birth
    birth_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1850), MaxValueValidator(2030)]
    )

    # Death
    death_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1850), MaxValueValidator(2030)]
    )

    # Admin and meta fields
    admin_notes = models.TextField(blank=True, null=True)
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    @property
    def name(self):
        names = [name for name in [self.title, self.first_name, self.last_name] if name]
        return " ".join(names) if len(names) else f"(no name, ID: {self.id})"

    def __str__(self):
        return self.name


class PersonHistory(models.Model):
    """
    Historical changes to a Person object, e.g. previous names, titles, etc.
    """

    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    other_names = models.CharField(max_length=255, blank=True, null=True)

    # Change start date
    start_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='start date (year)'
    )
    start_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='start date (month)'
    )
    start_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='start date (day)'
    )
    start_date_details = models.CharField(max_length=1000, blank=True, null=True)

    # Change end date
    end_date_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)],
        verbose_name='end date (year)'
    )
    end_date_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='end date (month)'
    )
    end_date_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name='end date (day)'
    )
    end_date_details = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'person histories'


# Relationship tables (M2M with additional fields)


class RelEntityAndEvent(models.Model):
    """
    M2M relationship between Entity and Event models
    """

    entity = models.ForeignKey(Entity, on_delete=models.RESTRICT)
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelEntityAndEvent, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelEntityAndItem(models.Model):
    """
    M2M relationship between Entity and Item models
    """

    entity = models.ForeignKey(Entity, on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelEntityAndItem, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelEntityAndPerson(models.Model):
    """
    M2M relationship between Entity and Person models
    """

    entity = models.ForeignKey(Entity, on_delete=models.RESTRICT)
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelEntityAndPerson, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelEventAndItem(models.Model):
    """
    M2M relationship between Event and Item models
    """

    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelEventAndItem, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelEventAndPerson(models.Model):
    """
    M2M relationship between Event and Person models
    """

    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelEventAndPerson, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelItemAndItem(models.Model):
    """
    M2M relationship between Item and Item models
    """

    item_1 = models.ForeignKey(Item, on_delete=models.RESTRICT, related_name='item_1')
    item_2 = models.ForeignKey(Item, on_delete=models.RESTRICT, related_name='item_2')
    type = models.ForeignKey(SlTypeRelItemAndItem, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)


class RelItemAndPerson(models.Model):
    """
    M2M relationship between Entity and Item models
    """

    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    person = models.ForeignKey(Person, on_delete=models.RESTRICT)
    type = models.ForeignKey(SlTypeRelItemAndPerson, on_delete=models.RESTRICT, blank=True, null=True)
    relationship_started = models.CharField(max_length=1000, blank=True, null=True)
    relationship_ended = models.CharField(max_length=1000, blank=True, null=True)
    relationship_details = models.TextField(blank=True, null=True)
