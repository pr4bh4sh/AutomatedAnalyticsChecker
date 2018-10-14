from behave import given, when, then, step
from delayed_assert import delayed_assert as das
from driver import Driver


@given('I open trivago magazine page')
def step_impl(context):
    pass
    # driver = Driver()
    # driver.get_driver()



@when('I wait for page view')
def step_impl(context):
    pass


@then('I match following params for page view')
def step_impl(context):
    for row in context.table:
        import ipdb
        ipdb.set_trace(context=5)
        val = row['name']
        das.expect()
