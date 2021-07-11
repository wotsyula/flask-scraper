#!/usr/bin/env python3
"""
Script that finds people on `google.com`

Searches for linkedin accounts, twitter accounts, facebook accounts.
"""

from logging import debug
from time import sleep
from typing import Generator
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
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

    def click_next_page_link(self):
        """
        Clicks on the next page link of google search results.
        """
        # click on next page link
        try:
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

    def go_to_next_page(self) -> bool:
        """
        Sends browser to next page.

        Returns:
            bool: Returns `True` if successful and `False` otherwise
        """
        # Don't try to scan beyound `max_page`
        if self.current_page < 1 or self.current_page >= self.max_page:
            return False

        # navigate to next page
        try:
            debug('Going to next page')
            self.scroll_to_bottom()
            self.click_next_page_link()

            if self.is_recaptcha():
                return self.solve_recaptcha()

            return True

        except (TimeoutException, NoSuchElementException):
            pass

        return False

    def go_to_page(self, page: int) -> bool:
        """
        Navigates to a specific page.

        Args:
            page (int): page to navigate to

        Returns:
            bool: `True` if successful and `False` otherwise
        """
        debug('Going to page: ' + str(page))

        while self.current_page < page:
            if not self.go_to_next_page():
                return False

        return True

    def scrape_results(self) -> Generator[dict, None, None]:
        """
        Generator function that scrapes search results on current page.

        Yields:
            Generator[dict, None, None]: search result
        """
        try:
            debug('Scraping results on page: ' + str(self.current_page))

            user_agent = self.user_agent

            for link in self.driver.find_elements(
                By.XPATH,
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
                    'page': self.current_page,
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
        while True:
            # get results for current page
            for result in self.scrape_results():
                for test_string in SOCIAL_SITES:
                    if test_string in result['href']:
                        yield result
                        break

            # go to next page
            if not self.go_to_next_page():
                break

    def execute(self, **kwargs) -> Generator[dict, None, None]:
        """
        Executes the script using `driver`.

        Args:
            **max_page (int): last page to scrape. Default to 99
            **page (int): Starting page to start execution. Default to 1
            **retries (int): number of times to retry execution. Default to 2
            **query (str): search string to find people. Default to ''
            **kwargs (dict[str, any]): Used to pass arguments to script


        Yields:
            Generator[dict, None, None]: Returns a list of `dict` values
        """
        options = {**self.options, **kwargs}
        self.max_page = options.pop('max_page', 99)
        page = options.pop('page', 1)
        retries = options.pop('retries', 2)
        query = options.pop('query', '')

        # exit early if no query
        if len(query) < 2:
            return

        try:
            # go to google.com website
            if 'google.com/search' not in self.driver.current_url:
                self.driver.get(URL)

            debug('Entering query: ' + query)

            query = query + SOCIAL_QUERY + Keys.ENTER

            self.send_keys('//*[@name="q"]', query, True)

            self.current_page = 1

            # navigate to start page
            self.go_to_page(page)

            # parse results
            yield from self.scrape()

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # no more attempts?
            if retries < 1:
                raise err

            # Try again
            self.driver.refresh()
            self.execute(**kwargs, retries=retries - 1)
