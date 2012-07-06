# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


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

        def fix_string(field):
            return field.value_to_string(self).encode("utf-8")

        meta_fields = BioModel._meta.fields
        return [(field, fix_string(field)) for field in meta_fields]
