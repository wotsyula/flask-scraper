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
BAD_REQUEST = {
    'status': 400,
    'error': 'Bad Request',
    'result': None,
}
class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

    def execute(self, user_name = '', user_pass = '',  **kwargs) -> Generator[dict, None, None]:
        """
        Attempts to log into website.

        Args:
            user_name (str, optional): email address of google user. Defaults to ''.
            user_pass (str, optional): password of google user. Defaults to ''.

        Raises:
            TimeoutException: if required elements are not found on page

        Yields:
            Generator[dict, None, None]: [description]
        """
        options = dict(**self.options, **kwargs)
        retries = options.pop('retries', 0)

        # exit early if no user name / pass
        if len(user_name) < 2 or len(user_pass) < 2:
            yield BAD_REQUEST

        try:
            # go to google.com website
            if 'google.com' not in str(self.driver.current_url):
                self.driver.get(URL)

            # click on login button
            self.click('//a[contains(@href, "google.com/ServiceLogin")]')

            # enter email address
            self.send_keys('//input[@type="email"]', user_name + Keys.ENTER, True)

            # enter password
            self.send_keys('//input[@type="password"]', user_pass + Keys.ENTER, True)

            # empty result
            yield {
                'status': 200,
                'error': None,
                'result': {
                    'time': round(time.time() * 1000),
                }
            }

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # 3rd attempt?
            if retries > 2:
                raise err
            else:
                retries += 1
                self.execute(retries=retries, **kwargs)
