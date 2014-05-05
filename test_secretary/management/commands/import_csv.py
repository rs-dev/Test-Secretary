import os
import csv

from django.core.management.base import BaseCommand, CommandError

from test_secretary.models import *

class Command(BaseCommand):
    args = '<csv file names>'
    help = 'Import testcases from csv'

    def handle(self, *args, **options):
        for fn in args:
            bfn = os.path.basename(fn)
            appname, sectionname = bfn.split('.')[0].split('_')
            print('Import for app: %s' % appname)
            print('import for section: %s' % sectionname)

            app, cr = Application.objects.get_or_create(name=appname)
            if cr:
                print('Create new app "%s"' % appname)

            section, cr = TestSection.objects.get_or_create(name=sectionname, app=app)
            if cr:
                print('Create new section "%s" for app "%s"' % (sectionname, appname))

            with open(fn) as f:
                for testcase in csv.DictReader(f, delimiter=';'):
                    preconditions = []
                    if not testcase['preconditions'] is None:
                        preconditions = testcase['preconditions'].split(',')
                    testcase.pop('preconditions', None)
                    tc, cr = TestCase.objects.get_or_create(section=section, **testcase)
                    if cr:
                        print('Create Testcase: %s' % tc.name)

                    for precondition in preconditions:
                        if precondition.isdigit():
                            tp = TestCase.objects.get(number=precondition, section=section)
                            tc.preconditions.add(tp)
