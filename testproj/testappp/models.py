# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from  django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.models import ContentType


class BioModel(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    bio = models.TextField()
    date_of_birth = models.DateField()
    email = models.EmailField()
    jabber = models.CharField(max_length=50)
    skype = models.CharField(max_length=50)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to="photo")

    class Meta:
        verbose_name = _('Bio')
        verbose_name_plural = _('Bios')

    def __unicode__(self):
        return  self.name

    def get_fields(self):
        fix = lambda x: x.value_to_string(self).encode("utf-8")
        return [(field, fix(field)) for field in BioModel._meta.fields]


class RequestModel(models.Model):
    create_data = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['-create_data']


class DBLogRecord(models.Model):
    body = models.CharField(max_length=256)

    def __unicode__(self):
        return self.body


def save_handler(sender, instance, created, **kwargs):
    log = None
    if isinstance(instance, DBLogRecord):
        return
    if created:

        log = DBLogRecord(
            body="{0} added pk = {1}".format(
                instance.__class__.__name__,
                instance.pk
            )
        )
    else:
        log = DBLogRecord(
            body="{0} changed pk = {1}".format(
                instance.__class__.__name__,
                instance.pk
            )
        )
    log.save()


def delete_handler(sender, instance, **kwargs):
    log = DBLogRecord(
        body="{0} deleted".format(instance.__class__.__name__)
    )
    log.save()


def create_content_model(sender, instance, created, **kwargs):
    if created and isinstance(instance, ContentType):
        pre_delete.connect(delete_handler, instance.model_class())
        post_save.connect(save_handler, instance.model_class())

post_save.connect(create_content_model, ContentType)
