# -*- coding: utf-8 -*-
__author__ = 'lex'
from django.test import TestCase
from testproj.testappp.models import BioModel
from datetime import datetime
from random import choice


class BasicTest(TestCase):
    def test_check_data(self):
        self.assertTrue(BioModel.objects.count() > 0)
        test_bio = BioModel.objects.all()[0]
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        for fied, value in test_bio.get_fields()[1:]:
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
