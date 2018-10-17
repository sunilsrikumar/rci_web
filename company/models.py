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



class CompanyIndexPage(Page):
    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('logo_image'),
        FieldPanel('intro', classname="full"),
    ]

class CompanyCareersPage(Page):
    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    career_page_heading=models.CharField(max_length=255, blank=True)
    career_page_subheading = models.CharField(max_length=255, blank=True)
    career_intro=RichTextField(blank=True)
    career_checklist_header=models.CharField(max_length=255, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('intro'),

    ]
    content_panels = Page.content_panels + [
        ImageChooserPanel('logo_image'),
        FieldPanel('name'),
        FieldPanel('intro', classname="full"),
        FieldPanel('career_page_heading'),
        FieldPanel('career_page_subheading'),
        FieldPanel('career_intro', classname="full"),
        ImageChooserPanel('image'),
        InlinePanel('career_work_culture', label="Career Work Culture"),
        InlinePanel('career_block', label="Career Block"),
        FieldPanel('career_checklist_header'),
    ]


class CareerWorkCulture(Orderable):
    page = ParentalKey(CompanyCareersPage, on_delete=models.CASCADE, related_name='career_work_culture')
    block_title = models.CharField(max_length=255, blank=True)
    block_intro = RichTextField(blank=True)
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
        FieldPanel('block_title'),
        FieldPanel('block_intro'),
        FieldPanel('embed_url'),
    ]

class Careerblock(Orderable):
    page = ParentalKey(CompanyCareersPage, on_delete=models.CASCADE, related_name='career_block')
    block_title = models.CharField(max_length=255, blank=True)
    block_intro = RichTextField(blank=True)
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
        FieldPanel('block_title'),
        FieldPanel('block_intro'),
        FieldPanel('embed_url'),
    ]


class CareerOpeningPage(Page):
    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    career_heading = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    front_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )



    search_fields = Page.search_fields + [
        index.SearchField('career_heading'),
        index.SearchField('intro'),

    ]
    content_panels = Page.content_panels + [
        ImageChooserPanel('logo_image'),
        ImageChooserPanel('front_image'),
        FieldPanel('career_heading'),
        FieldPanel('intro', classname="full"),
    ]
