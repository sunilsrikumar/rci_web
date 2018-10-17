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




from wagtail.snippets.models import register_snippet

# A couple of abstract classes that contain commonly used fields



class HomePage(Page):
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('logo_image'),
        FieldPanel('body', classname="full"),
        InlinePanel('carousel_images', label="Carousel images"),
        InlinePanel('gallery_images', label="Gallery images"),
        InlinePanel('feature_images', label="Feature images"),
        InlinePanel('section_images', label="Section images"),
        InlinePanel('section_blog_images', label="Section Blog images"),
        InlinePanel('section_case_study_images', label="Section Case Study images"),

    ]

# Carousel items

class CarouselItem(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_images')
    caption = models.CharField(max_length=255, blank=True)
    tag_line = models.CharField(max_length=250,blank=True,null=True)
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
        FieldPanel('caption'),
        FieldPanel('tag_line'),
        FieldPanel('embed_url'),
    ]


class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='gallery_images')
    caption = models.CharField(blank=True,null=True, max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class HomePageFeatureImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='feature_images')
    header = models.CharField(blank=True,null=True, max_length=250)
    intro = models.CharField(blank=True,null=True, max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('header'),
        FieldPanel('intro'),
    ]

class HomePageSectionImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='section_images')
    caption = models.CharField(blank=True,null=True, max_length=250)
    intro = models.CharField(blank=True,null=True, max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('intro'),
    ]


class HomePageSectionBlogImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='section_blog_images')
    caption = models.CharField(blank=True,null=True, max_length=250)
    intro = models.CharField(blank=True,null=True, max_length=250)

    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('blog_image'),
        FieldPanel('caption'),
        FieldPanel('intro'),
    ]

class HomePageSectionCaseStudyImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='section_case_study_images')
    caption = models.CharField(blank=True,null=True, max_length=250)
    intro = models.CharField(blank=True,null=True, max_length=250)

    case_study_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('case_study_image'),
        FieldPanel('caption'),
        FieldPanel('intro'),
    ]


# Forms
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


    full_name = models.CharField(max_length=255,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    company=models.CharField(max_length=222,blank=True,null=True)
    phone=models.CharField(max_length=222,blank=True,null=True)
    message = RichTextField(blank=True)

    panels = [
        FieldPanel('full_name'),
        FieldPanel('email'),
        FieldPanel('company'),
        FieldPanel('phone'),
        FieldPanel('message'),
    ]




class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]