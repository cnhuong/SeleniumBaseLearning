"""

In Python, the code class TimeLimitExceededException(Exception): pass defines a new exception class named
TimeLimitExceededException that inherits from the built-in Exception class.

Let's break down the components:

class: This keyword is used to define a new class.

TimeLimitExceededException: This is the name of the new exception class. The convention in Python is to name exception
classes with names ending in "Error" or "Exception" to make it clear that they represent exceptional situations.

(Exception): This indicates that TimeLimitExceededException is inheriting from the built-in Exception class.
In Python, exceptions are typically defined by creating a new class that inherits from a built-in exception class.

pass: The pass statement is a no-operation statement in Python. It serves as a placeholder where syntactically some code
is required, but you don't want to perform any action. In this case, it's used to indicate that the body of the class is
empty.
"""


import unittest
from seleniumbase.common.exceptions import (
    NoSuchWindowException,
    OutOfScopeException
)


class BaseCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initialize_variables()

    def __initialize_variables(self):
        self.driver = None
        self.__extra_actions = []

    def _check_browser(self):
        """This method raises an exception if the active window is closed.
        (This provides a much cleaner exception message in this situation.)"""
        active_window = None
        try:
            active_window = self.driver.current_window_handle  # Fails if None
        except Exception:
            pass
        if not active_window:
            raise NoSuchWindowException("Active window was already closed!")

    def execute_script(self, script, *args, **kwargs):
        self.__check_scope()
        self._check_browser()
        return self.driver.execute_script(script, *args, **kwargs)

    def __check_scope(self):
        if hasattr(self, "browser"):  # self.browser stores the type of browser
            return  # All good: setUp() already initialized variables in "self"
        else:
            message = (
                "\n It looks like you are trying to call a SeleniumBase method"
                "\n from outside the scope of your test class's `self` object,"
                "\n which is initialized by calling BaseCase's setUp() method."
                "\n The `self` object is where all test variables are defined."
                "\n If you created a custom setUp() method (that override the"
                "\n the default one), make sure to call super().setUp() in it."
                "\n When using page objects, be sure to pass the `self` object"
                "\n from your test class into your page object methods so that"
                "\n they can call BaseCase class methods with all the required"
                "\n variables, which are initialized during the setUp() method"
                "\n that runs automatically before all tests called by pytest."
            )
            raise OutOfScopeException(message)

    def get_current_url(self):
        self.__check_scope()
        current_url = self.driver.current_url
        if "%" in current_url:
            try:
                from urllib.parse import unquote
                current_url = unquote(current_url, errors="strict")
            except Exception:
                pass
        return current_url

    def __is_valid_storage_url(self):
        url = self.get_current_url()
        if url and len(url) > 0:
            if "http:" in url or "https:" in url or "file:" in url:
                return True
        return False

    def clear_local_storage(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            return
        self.execute_script("window.localStorage.clear();")
