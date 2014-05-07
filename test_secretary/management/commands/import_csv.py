import os
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from test_secretary.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--legacy',
            action='store_true',
            dest='legacy',
            default=False,
            help='Use legacy syntax for doc csv extraction'),
    )
    args = '<csv file names>'
    help = 'Import testcases from csv'

    def _preprocess(self, testcase):
        processed = {}
        #;testcase;description;pre-condition;input-data;expected-behavior;actual-behavior
        mapping = (('pre-condition', 'precondition_comment'),
                   ('#', 'number'), ('testcase', 'name'),
                   ('description', 'description'),
                   ('expected-behavior', 'expected'),
                   ('input-data', 'action'))
        for mp in mapping:
            if mp[0] in testcase and testcase[mp[0]]:
                processed[mp[1]] = testcase[mp[0]]
        return processed

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
                    if 'legacy' in options and options['legacy']:
                        testcase = self._preprocess(testcase)

                    preconditions = []
                    if 'preconditions' in testcase and not testcase['preconditions'] is None:
                        preconditions = testcase['preconditions'].split(',')
                    testcase.pop('preconditions', None)

                    tcs = TestCase.objects.filter(section=section, name=testcase['name'])
                    if tcs.count() == 0:
                        tc = TestCase.objects.create(section=section, active=True, **testcase)
                        print('Create Testcase: %s' % tc.name)
                    elif tcs.count() == 1:
                        tc = tcs[0]
                    else:
                        print('Found multiple testcases with same name in section:', tcs)
                        print('Take first testcase')
                        tc = tcs[0]

                    for precondition in preconditions:
                        if precondition.isdigit():
                            tp = TestCase.objects.get(number=precondition, section=section)
                            tc.preconditions.add(tp)
