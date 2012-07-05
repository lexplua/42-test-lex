# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from  django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class BioModel(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    bio = models.TextField()
    date_of_birth = models.DateField()
    email = models.EmailField()
    jabber = models.CharField(max_length=50)
    skype = models.CharField(max_length=50)
    other_contacts = models.TextField()

    class Meta:
        verbose_name = _('Bio')
        verbose_name_plural = _('Bios')

    def __unicode__(self):
        return  self.name

    def get_fields(self):
        # make a list of field/values.
        return [(field, field.value_to_string(self).encode("utf-8")) for field in BioModel._meta.fields]

class RequestModel(models.Model):
    create_data = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['-create_data']

class DBLogRecord(models.Model):
    body = models.CharField(max_length=256)

    def __unicode__(self):
        return self.body


def get_subclasses(classes, level=0):
    """
        Return the list of all subclasses given class (or list of classes) has.
        Inspired by this question:
        http://stackoverflow.com/questions/3862310/how-can-i-find-all-subclasses-of-a-given-class-in-python
    """
    # for convenience, only one class can can be accepted as argument
    # converting to list if this is the case
    if not isinstance(classes, list):
        classes = [classes]

    if level < len(classes):
        classes += classes[level].__subclasses__()
        return get_subclasses(classes, level+1)
    else:
        return classes




def save_handler(sender,instance,created,**kwargs):
    log=None
    if isinstance(instance,DBLogRecord):return
    if created:

        log = DBLogRecord(
            body = ' '.join((instance.__class__.__name__,"added","pk = {0}".format(instance.pk)))
        )
    else:
        log = DBLogRecord(
            body = ' '.join((instance.__class__.__name__,"changed","pk = {0}".format(instance.pk)))
        )
    log.save()

def delete_handler(sender,instance,**kwargs):
    log = DBLogRecord(
        body = ' '.join((instance.__class__.__name__,"deleted"))
    )
    log.save()

for model in [User, BioModel, RequestModel]:
    pre_delete.connect(delete_handler,model)
    post_save.connect(save_handler,model)