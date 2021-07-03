#!/usr/bin/env python3
"""
Script that finds people on `google.com`

Searches for linkedin accounts, twitter accounts, facebook accounts.
"""

from time import sleep
from typing import Generator
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.keys import Keys

from ..script import Script as BaseClass

URL = 'https://www.google.com'
SOCIAL_QUERY = ' (inurl:linkedin|inurl:twitter|inurl:facebook)'
SOCIAL_SITES = ['twitter.com/', 'facebook.com/', 'linkedin.com/in/']

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

    def click_next_link(self):
        """
        Clicks on the next page link of google search results.
        """
        try:
            # click on next page link
            text = str(self.current_page + 1)

            self.sleep(4)
            self.click(
                f'(//footer//*[contains(text(),">")]|//*[text()="{text}"]|//h3/div[@class])[last()]'
            )

            # update page pointer
            self.current_page += 1

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            # click show ommited results link
            self.click('//*[contains(@href, "filter=0")]')

            # update page pointer
            self.current_page = 1

        sleep(5)

    def go_to_next(self) -> bool:
        """
        Sends browser to next page.

        Returns:
            bool: Returns `True` if successful and `False` otherwise
        """
        # Don't try to scan more than 99 pages
        if self.current_page < 1 or self.current_page > 98:
            return False

        try:
            self.scroll_to_bottom()

            self.click_next_link()

            if self.is_recaptcha():
                return self.solve_recaptcha()

            return True

        except (TimeoutException, NoSuchElementException):
            pass

        return False


    def scrape_results(self) -> Generator[dict, None, None]:
        """
        Generator function that scrapes search results on current page.

        Yields:
            Generator[dict, None, None]: search result
        """
        try:
            user_agent = self.user_agent()

            for link in self.driver.find_elements_by_xpath(
                '//*[@id="search" or @id="rso" or @id="main"]//a[@href]',
            ):
                href: str = link.get_attribute('href')

                if \
                    len(link.text) < 4 \
                    or 'google.com' in href and not 'google.com/url?' in href \
                    or 'googleusercontent.com' in href \
                :
                    continue

                yield {
                    'href': href,
                    'text': link.text,
                    'userAgent': user_agent,
                    'referer': self.driver.current_url,
                }

        except (TimeoutException, NoSuchElementException):
            pass

    def scrape(self) -> Generator[dict, None, None]:
        """
        Generator function that scrapes search results on current all pages.

        Yields:
            Generator[dict, None, None]: search result
        """
        # set current page
        self.current_page = 1

        while True:
            # get results for current page
            for result in self.scrape_results():
                for test_string in SOCIAL_SITES:
                    if test_string in result['href']:
                        yield result
                        break

            # go to next page
            if not self.go_to_next():
                break

    def execute(self, **kwargs) -> Generator[dict, None, None]:
        options = {**self.options, **kwargs}
        query = options.pop('query', '')
        retries = options.pop('retries', 0)

        # exit early if no query
        if len(query) < 2:
            return

        try:
            # go to google.com website
            if 'google.com/search' not in self.driver.current_url:
                self.driver.get(URL)

            # enter query
            new_query = query + SOCIAL_QUERY + Keys.ENTER

            self.send_keys('//*[@name="q"]', new_query, True)

            self.current_page = 1

            # parse results
            yield from self.scrape()

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # 3rd attempt?
            if retries > 2:
                raise err

            # Try again
            else:
                self.execute(retries=retries + 1, **kwargs)
