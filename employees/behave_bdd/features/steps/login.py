from behave import *


@Given("Open the Odoo Page")
def open_the_odoo_page(context):
    sb = context.sb
    sb.open("https://runbot.odoo.com/")
    sb.clear_local_storage()


@step("Login to Swag Labs with {user}")
def login_to_swag_labs(context, user):
    sb = context.sb
    sb.type("#user-name", user)
    sb.type("#password", "secret_sauce\n")


@step("Verify that the current user is logged in")
def verify_logged_in(context):
    sb = context.sb
    sb.assert_element("#header_container")
    sb.assert_element("#react-burger-menu-btn")
    sb.assert_element("#shopping_cart_container")
