# -*- coding: utf-8 -*-
__author__ = 'lex'
from django.test import TestCase
from testproj.testappp.models import BioModel,DBLogRecord
from datetime import datetime
from random import randrange,choice
from django.conf import settings
from django.contrib.auth.models import User

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
        del user
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "User deleted").count())
        bio = BioModel(
            name = "Test",
            lastname = "Test",
            bio = "pass",
            date_of_birth="11.11.2011",
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
        del bio
        self.assertTrue(DBLogRecord.objects.filter(body__exact = "BioModel deleted").count())

        self.assertTrue(logs.filter(body__startswith = "DBLogRecord added").count()==6)