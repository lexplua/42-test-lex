from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    args = '<out>'
    help = 'Print all project models and the count of objects in every model'

    def handle(self, *args, **options):
        models = [x.model_class() for x in ContentType.objects.all()]
        for model in models:
            self.stdout.write(
                "{0} : {1} instanses\n".format(
                    model.__name__, model.objects.all().count()
                )
            )
            self.stderr.write(
                "error: {0} : {1} instanses\n".format(
                    model.__name__, model.objects.all().count()
                )
            )
