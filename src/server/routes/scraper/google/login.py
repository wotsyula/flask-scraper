#!/usr/bin/env python3
"""
Script that logs into `google.com`
"""

from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from ..script import Script as BaseClass

URL = 'https://www.google.com'

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

    def execute(self, **kwargs) -> list[dict]:
        """
        Attempts to log into website.
        """
        result = []
        options = dict(**self.options, **kwargs)
        user_name = str(options.get('user_name', ''))
        user_pass = str(options.get('user_pass', ''))
        retries = options.get('retries', 0)

        # exit early if no user name / pass
        if len(user_name) < 2 or len(user_pass) < 2:
            return result

        try:
            # go to google.com website
            self.driver.get(URL)

            # click on login button
            self.click('//a[contains(@href, "google.com/ServiceLogin")]')

            # enter email address
            field = self.send_keys('//input[@type="email"]', user_name, True)

            field.send_keys(Keys.ENTER)

            # enter password
            field = self.send_keys('//input[@type="password"]', user_pass, True)

            field.send_keys(Keys.ENTER)

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # 3rd attempt?
            if retries > 2:
                raise err
            else:
                return self.execute(retries = retries + 1, **kwargs)

        return result
