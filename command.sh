#!/bin/bash
OF=$(date +%Y%m%d).dat
PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings django-admin.py modelscount 2>$OF
