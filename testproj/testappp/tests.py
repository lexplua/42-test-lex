# -*- coding: utf-8 -*-
__author__ = 'lex'
from django.test import TestCase
from testproj.testappp.models import BioModel

class BasicTest(TestCase):
    def test_check_data(self):
        self.assertTrue(BioModel.objects.count()>0)
        test_bio = BioModel.objects.all()[0]
        resp = self.client.get("/")
        self.assertEqual(resp.status_code,200)
        for fied, value in test_bio.get_fields()[1:]:
            self.assertIn(value, resp.content)