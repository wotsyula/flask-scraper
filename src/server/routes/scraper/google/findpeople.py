#!/usr/bin/env python3
"""
Script that finds people on `google.com`

Searches for linkedin accounts, twitter accounts, facebook accounts.
"""

from typing import Generator
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys

from ..script import Script as BaseClass

URL = 'https://www.google.com'

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """

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
            # navigate to bottom of page
            self.send_keys('//*[@name="q"]', Keys.PAGE_DOWN + Keys.PAGE_DOWN + Keys.END)

            try:
                # click show ommited results link
                self.click('//*[contains(@href, "filter=0")]')

                # update page pointer
                self.current_page = 1

                return True

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                pass

            # click on next page link
            link_text = str(self.current_page + 1)

            self.driver.find_element_by_link_text(link_text).click()
            self.sleep(4)

            # check current page
            expected_text = ' ' + link_text + ' '
            stat_text = self.xpath('//*[@id="result-stats"]').text

            if expected_text in stat_text:
                # update page pointer
                self.current_page += 1
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
            for link in self.driver.find_elements_by_xpath('//*[@class="g"]//a[@href]'):
                href: str = link.get_attribute('href')
                
                if 'google.com' in href or 'googleusercontent.com' in href:
                    continue

                yield {
                    'href': href,
                    'text': link.text,
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

        # get results for current page
        for result in self.scrape_results():
            for test_string in ['twitter.com/', 'facebook.com/', 'linkedin.com/in/']:
                if test_string in result['href']:
                    yield result
                    break

        # go to next page
        while self.go_to_next():
            # get results for next page
            for result in self.scrape_results():
                for test_string in ['twitter.com/', 'facebook.com/', 'linkedin.com/in/']:
                    if test_string in result['href']:
                        yield result
                        break

    def execute(self, **kwargs) -> Generator[dict, None, None]:
        options = dict(**self.options, **kwargs)
        query = str(options.pop('query', ''))
        retries = options.pop('retries', 0)

        # exit early if no query
        if len(query) < 2:
            return

        try:
            # go to google.com website
            if 'google.com/search' not in self.driver.current_url:
                self.driver.get(URL)

            # enter query
            self.send_keys('//*[@name="q"]' + Keys.ENTER, query, True)

            self.current_page = 1

            # parse results
            self.scrape()

        except NoSuchElementException:
            pass

        except TimeoutException as err:
            # 3rd attempt?
            if retries > 2:
                raise err
            else:
                self.execute(retries = retries + 1, **kwargs)
