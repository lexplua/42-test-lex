# -*- coding: utf-8 -*-
__author__ = 'lex'
from django.test import TestCase
from testproj.testappp.models import BioModel, DBLogRecord, RequestModel
from datetime import datetime
from random import choice
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.core import management
import sys


class BasicTest(TestCase):
    def test_check_data(self):
        self.assertTrue(BioModel.objects.count() > 0)
        test_bio = BioModel.objects.all()[0]
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        for field, value in test_bio.get_fields()[1:]:
            self.assertIn(value, resp.content)


class MiddlewareTest(TestCase):
    def test_check_data(self):
        data = []
        for i in range(5):
            now_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            resp = self.client.get(choice(("/", "/requests/")))
            data.append(now_date)
        resp = self.client.get("/requests/")
        self.assertEqual(resp.status_code, 200)
        for i in data:
            self.assertIn(i, resp.content)


class ContextProcessorTest(TestCase):
    def test_check_data(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('settings' in resp.context)
        self.assertEqual(settings, resp.context['settings'])


class SignalHandlerTest(TestCase):
    def test_check_data(self):
        user = User.objects.create_user("testuser", "test@test.ua", "password")
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="User added pk = {0}".format(user.pk)
            ).count())
        user.is_superuser = True
        user.save()
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="User changed pk = {0}".format(user.pk)
            ).count())
        user.delete()
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="User deleted"
            ).count())
        bio = BioModel(
            name="Test",
            lastname="Test",
            bio="pass",
            date_of_birth="2011-11-11",
            email="test@test.ua",
            jabber="test@test.ua",
            skype="test",
            other_contacts="pass"
        )
        bio.save()
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="BioModel added pk = {0}".format(bio.pk)
            ).count())
        bio.name = "other"
        bio.save()
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="BioModel changed pk = {0}".format(bio.pk)
            ).count())
        bio.delete()
        self.assertTrue(
            DBLogRecord.objects.filter(
                body__exact="BioModel deleted"
            ).count())


class FormTest(TestCase):
    def login_test(self):
        resp = self.client.get('/')
        self.assertIn('Edit', resp.content)
        self.client.login(username='admin', password='admin')

    def edit_form_test(self):
        data_dict = {
            'name': 'test',
            'lastname': 'testlastname',
            'bio': 'testbio',
            'date_of_birth': '2013-11-11',
            'email': 'testemail@gmail.com',
            'jabber': 'testjabber@gmail.com',
            'skype': 'testskype',
            'other_contacts': 'test_other_contacts',
            'photo': open(os.path.join(settings.MEDIA_ROOT, 'me.jpg')),
        }
        self.client.post('/editbio/', data_dict)
        resp = self.client.get('/editbio/')
        for key, data in data_dict.iteritems():
            if key != 'photo':
                self.assertIn(data, resp.content)

    def test_check_data(self):
        self.login_test()
        self.edit_form_test()


class TagTest(TestCase):
    def login_test(self):
        resp = self.client.get('/')
        self.assertIn('Edit', resp.content)
        self.client.login(username='admin', password='admin')

    def test_check_data(self):
        self.login_test()
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('/admin/auth/user/1/', resp.content)


class CommandTest(TestCase):
    def test_check_data(self):

        class MyStdOut(object):
            def __init__(self):
                self.data = ''

            def write(self, s):
                self.data += s

        my_out = MyStdOut()
        sys.stdout = my_out
        management.call_command('modelscount')
        self.assertIn(
            "{0} : {1} instanses\n".format("User",
            User.objects.all().count()), my_out.data
        )
        self.assertIn("{0} : {1} instanses\n".format(
            "BioModel",
            BioModel.objects.all().count()), my_out.data
        )
        self.assertIn("{0} : {1} instanses\n".format(
            "DBLogRecord",
            DBLogRecord.objects.all().count()), my_out.data
        )
        self.assertIn("{0} : {1} instanses\n".format(
            "RequestModel",
            RequestModel.objects.all().count()), my_out.data
        )


class TestAjax(TestCase):
    def login_test(self):
        resp = self.client.get('/')
        self.assertIn('Edit', resp.content)
        self.assertTrue(self.client.login(username='admin', password='admin'))

    def edit_form_test(self):
        data_dict = {
            'name': 'test',
            'lastname': 'testlastname',
            'bio': 'testbio',
            'date_of_birth': ' 2013-11-11',
            'email': 'testemail@gmail.com',
            'jabber': 'testjabber@gmail.com',
            'skype': 'testskype',
            'other_contacts': 'test_other_contacts',
            'photo': open(os.path.join(settings.MEDIA_ROOT, 'me.jpg')),
        }
        resp = self.client.post(
            '/editbio/',
            data_dict,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        print resp.content
        resp = self.client.get('/editbio/')
        for key, data in data_dict.iteritems():
            if key != 'photo':
                self.assertIn(data, resp.content)

    def test_check_data(self):
        self.login_test()


class TestT13(TestCase):
    def check_test_data(self):
        self.client.get('/test1/')
        self.client.get('/test2/')
        self.client.get('/test3/')
        self.client.get('/test4/')
        self.client.get('/test5/')
        record1 = RequestModel.objects.filter(body__icontains='test1/')[0]
        record2 = RequestModel.objects.filter(body__icontains='test2/')[0]
        record3 = RequestModel.objects.filter(body__icontains='test3/')[0]
        record4 = RequestModel.objects.filter(body__icontains='test4/')[0]
        record5 = RequestModel.objects.filter(body__icontains='test5/')[0]
        record1.priority = 1
        record1.save()
        record2.priority = 2
        record2.save()
        record3.priority = 3
        record3.save()
        record4.priority = 4
        record4.save()
        record5.priority = 5
        record5.save()

        testpage = self.client.get('/requests/').content

        self.assertTrue(testpage.index('/test1/') < testpage.index('/test2/'))
        self.assertTrue(testpage.index('/test2/') < testpage.index('/test3/'))
        self.assertTrue(testpage.index('/test3/') < testpage.index('/test4/'))
        self.assertTrue(testpage.index('/test4/') < testpage.index('/test5/'))
