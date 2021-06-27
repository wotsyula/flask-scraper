#!/usr/bin/env python3
"""
Script that logs into `google.com`
"""

import time
from typing import Generator
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from ..script import Script as BaseClass

URL = 'https://www.google.com'

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

    def execute(self, **kwargs) -> Generator[dict, None, None]:
        """
        Attempts to log into website.
        """
        options = dict(**self.options, **kwargs)
        user_name = str(options.get('user_name', ''))
        user_pass = str(options.get('user_pass', ''))
        retries = options.get('retries', 0)

        # exit early if no user name / pass
        if len(user_name) < 2 or len(user_pass) < 2:
            return

        try:
            # go to google.com website
            if 'google.com' not in self.driver.current_url:
                self.driver.get(URL)

            # click on login button
            self.click('//a[contains(@href, "google.com/ServiceLogin")]')

            # enter email address
            self.send_keys('//input[@type="email"]' + Keys.ENTER, user_name, True)

            # enter password
            self.send_keys('//input[@type="password"]' + Keys.ENTER, user_pass, True)

            yield {
                'time': round(time.time() * 1000),
            }

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # 3rd attempt?
            if retries > 2:
                raise err
            else:
                self.execute(retries = retries + 1, **kwargs)
