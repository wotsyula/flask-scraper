#!/usr/bin/env python3
"""
Script that logs into `google.com`
"""
from logging import debug
from typing import Generator
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from ..script import Script as BaseClass

URL = 'https://www.google.com'
BAD_REQUEST = 400
UNAUTHORIZED = 401
SUCCESS = 200

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

    def goto_login_page(self):
        """
        Navigates to login page.
        """
        if self.exists('//*[contains(@href, "google.com/Logout")]'):
            debug('User already logged in')
            return False

        debug('going to login page')

        # click login button
        self.click('//a[contains(@href, "google.com/ServiceLogin")]')

        # check for input field
        if not self.exists('//input[@type="email"]'):
            # click on use another account button
            self.click('(//*[@tabindex="0"])[last()-2]')

        return True

    def execute(self, **kwargs) -> Generator[dict, None, None]:
        """
        Attempts to log into website.

        Args:
            **max_page (int): last page to scrape. Default to 99
            **page (int): Starting page to start execution. Default to 1
            **retries (int): number of times to retry execution. Default to 2
            **user_name (str, optional): email address of google user. Defaults to SERVER_EMAIL.
            **user_pass (str, optional): password of google user. Defaults to SERVER_SECRET.
            **kwargs (dict[str, any]): Used to pass arguments to script

        Raises:
            TimeoutException: if required elements are not found on page

        Yields:
            Generator[dict, None, None]: [description]
        """
        options = {**self.options, **kwargs}
        self.max_page = options.pop('max_page', 99)
        # page = options.pop('page', 1)
        retries = options.pop('retries', 2)
        user_name = options.pop('user_name', '')
        user_pass = options.pop('user_pass', '')
        retries = options.pop('retries', 2)

        # exit early if no user name / pass
        if len(user_name) < 2 or len(user_pass) < 2:
            yield BAD_REQUEST
            return

        try:
            self.driver.get(URL)

            if self.goto_login_page():
                debug('Entering email address')
                self.send_keys('//input[@type="email"]', user_name + Keys.ENTER, True)
                self.sleep(5)

                debug('Entering password')
                self.send_keys('//input[@type="password"]', user_pass + Keys.ENTER, True)
                self.sleep(10)

            yield SUCCESS

        except NoSuchElementException:
            # failure
            yield UNAUTHORIZED

        except TimeoutException as err:
            # no more attempts?
            if retries < 1:
                raise err

            # Try again
            self.execute(**kwargs, retries=retries - 1)
