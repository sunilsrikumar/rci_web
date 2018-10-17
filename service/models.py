from __future__ import unicode_literals
from django.shortcuts import render
from django.db import models
import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page,Orderable
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index



class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('service_index_items', label="Service Index Items"),

    ]

class ServiceIndexItems(Orderable):
    page = ParentalKey(ServiceIndexPage, on_delete=models.CASCADE, related_name='service_index_items')
    heading1 = models.CharField(max_length=255, blank=True)
    heading2 = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('heading1'),
        FieldPanel('heading2'),

    ]


class ServicePage(Page):
    service_name = models.CharField(max_length=255, blank=True)
    service_intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('service_name'),
        index.SearchField('service_intro'),

    ]
    content_panels = Page.content_panels + [
        FieldPanel('service_name'),
        FieldPanel('service_intro', classname="full"),
        ImageChooserPanel('image'),

    ]

class MobileAppPage(Page):
    mobile_app_name = models.CharField(max_length=255, blank=True)
    mobile_app_intro = RichTextField(blank=True)
    mobile_service_title = models.CharField(max_length=255, blank=True)
    mobile_feature_title = models.CharField(max_length=255, blank=True)

    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'

    )

    search_fields = Page.search_fields + [
        index.SearchField('mobile_app_name'),
        index.SearchField('mobile_app_intro'),

    ]
    content_panels = Page.content_panels + [
        FieldPanel('mobile_app_name'),
        ImageChooserPanel('logo_image'),
        FieldPanel('mobile_app_intro', classname="full"),
        FieldPanel('mobile_service_title'),
        InlinePanel('service_item', label="Service Item"),
        FieldPanel('mobile_feature_title'),
        InlinePanel('feature_item', label="Feature Item"),

    ]



class ServiceItem(Orderable):
    page = ParentalKey(MobileAppPage, on_delete=models.CASCADE, related_name='service_item')
    service_title = models.CharField(max_length=255, blank=True)
    service_intro = RichTextField(blank=True)
    embed_url = models.URLField("Embed URL", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'

    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('service_title'),
        FieldPanel('service_intro'),
        FieldPanel('embed_url'),
    ]


class FeatureItem(Orderable):
    page = ParentalKey(MobileAppPage, on_delete=models.CASCADE, related_name='feature_item')
    feature_title = models.CharField(max_length=255, blank=True)
    feature_intro = RichTextField(blank=True)
    embed_url = models.URLField("Embed URL", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'

    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('feature_title'),
        FieldPanel('feature_intro'),
        FieldPanel('embed_url'),
    ]

