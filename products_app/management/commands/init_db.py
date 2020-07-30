from django.core.management.base import BaseCommand
from django.utils import timezone
from products_app import tasks


class Command(BaseCommand):
    help = 'Init database from Open Food Facts datas'

    def add_arguments(self, parser):
        parser.add_argument('-w', '--wishes', action='store_true', help='just to add new wishes in database')

    def handle(self, *args, **kwargs):
        wishes = kwargs['wishes']
        time = timezone.now().strftime('%X')
        print("loading data started at %s" % time)
        tasks.init_db(not wishes)
        time = timezone.now().strftime('%X')
        print("loading data ended at %s" % time)
