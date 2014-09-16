from django import template

register = template.Library()


@register.filter
def has_testcase_assigned(testrun, testcase):
    if testrun is None or testcase is None:
        return False
    return testrun.has_testcase_assigned(testcase)
