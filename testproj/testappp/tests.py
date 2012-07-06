# -*- coding: utf-8 -*-
__author__ = 'lex'
from django.test import TestCase
from testproj.testappp.models import BioModel,DBLogRecord
from datetime import datetime
from random import randrange,choice
from django.conf import settings
from django.contrib.auth.models import User
import os

class BasicTest(TestCase):
    def test_check_data(self):
        self.assertTrue(BioModel.objects.count()>0)
        test_bio = BioModel.objects.all()[0]
        resp = self.client.get("/")
        self.assertEqual(resp.status_code,200)
        for fied, value in test_bio.get_fields()[1:]:
            self.assertIn(value, resp.content)

class MiddlewareTest(TestCase):
    def test_check_data(self):
        data = []
        for i in range(5):
            now_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            resp = self.client.get(choice(("/","/requests/")))
            data.append(now_date)
        resp = self.client.get("/requests/")
        self.assertEqual(resp.status_code,200)
        for i in data:
            self.assertIn(i, resp.content)

class ContextProcessorTest(TestCase):
    def test_check_data(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('settings' in resp.context)
        self.assertEqual(settings,resp.context['settings'])

class SignalHandlerTest(TestCase):
    def test_check_data(self):
        user = User.objects.create_user("testuser","test@test.ua","password")
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "User added pk = {0}".format(user.pk)).count())
        user.is_superuser = True
        user.save()
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "User changed pk = {0}".format(user.pk)).count())
        user.delete()
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "User deleted").count())
        bio = BioModel(
            name = "Test",
            lastname = "Test",
            bio = "pass",
            date_of_birth="2011-11-11",
            email= "test@test.ua",
            jabber = "test@test.ua",
            skype = "test",
            other_contacts = "pass"
        )
        bio.save()
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "BioModel added pk = {0}".format(bio.pk)).count())
        bio.name = "other"
        bio.save()
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "BioModel changed pk = {0}".format(bio.pk)).count())
        bio.delete()
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "BioModel deleted").count())

class FormTest(TestCase):
    def login_test(self):
        resp = self.client.get('/')
        self.assertIn('Login',resp.content)
        self.assertNotIn('Edit',resp.content)
        self.client.login(username='lex',password='123123')
        resp = self.client.get('/')
        self.assertNotIn('Login',resp.content)
        self.assertIn('Edit',resp.content)

    def edit_form_test(self):
        data_dict={
            'name':'test',
            'lastname':'testlastname',
            'bio':'testbio',
            'date_of_birth':'2013-11-11',
            'email':'testemail@gmail.com',
            'jabber':'testjabber@gmail.com',
            'skype':'testskype',
            'other_contacts':'test_other_contacts',
            'photo':open(os.path.join(settings.MEDIA_ROOT,'me.jpg')),
        }
        self.client.post('/editbio/',data_dict)
        resp=self.client.get('/editbio/')
        for key,data in data_dict.iteritems():
            if key!='photo':
                self.assertIn(data,resp.content)

    def test_check_data(self):
        self.login_test()
        self.edit_form_test()