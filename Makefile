MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) test testappp

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) collectstatic --noinput
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) syncdb --noinput
dump:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) dumpdata --indent=2 auth > testproj/fixtures/initial_data.json
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproj.settings $(MANAGE) dumpdata --indent=2 testappp > testproj/testappp/initial_data.json
