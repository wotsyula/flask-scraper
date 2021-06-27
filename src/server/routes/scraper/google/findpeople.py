#!/usr/bin/env python3
"""
Script that finds people on `google.com`

Searches for linkedin accounts, twitter accounts, facebook accounts.
"""

from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
        result = []
        options = dict(**self.options, **kwargs)
        query = str(options.get('query', ''))
        retries = options.get('retries', 0)

        # exit early if no query
        if len(query) < 2:
            return result

        try:
            # go to google.com website
            self.driver.get(URL)

            # enter query
            field = self.send_keys('//*[@name="q"]', query, True)

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
