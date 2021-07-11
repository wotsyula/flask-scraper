#!/usr/bin/env python3
"""
Defines functions and classes for managing `Scraper` object.
"""
from concurrent.futures import ThreadPoolExecutor, Future
from logging import debug
import os
import time
from typing import Generator
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Remote as WebDriver, ChromeOptions

from .script import Script, create_script

CHROME_URI = os.environ.get('SELENIUM_URI', 'http://localhost:4444')
CHROME_USER_AGENT   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                    + 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    + 'Chrome/91.0.4472.101 ' \
                    + 'Safari/537.36 OPR/77.0.4054.90'


def create_driver(**kwargs) -> WebDriver:
    """
    Creates a selenium `Webdriver` instance.

    Args:
        **timeout (int): Value sent to `driver.implicitly_wait`. Defaults to 10
        **user_agent (str): User Agent header. Default to `CHROME_USER_AGENT`
        **save_session (bool): if `True` then current session will be stored and loaded.
                               Default to `False`
        **kwargs (any): All extra arguments are forwarded to seleniums `Webdriver()`
                        constructor

    Returns:
        WebDriver: instance to use for scrapping
    """
    options = {**kwargs}
    timeout = options.pop('timeout', 10)
    user_agent = options.pop('user_agent', CHROME_USER_AGENT)
    save_session = options.pop('save_session', False)

    # create driver options
    chrome_options = ChromeOptions()

    # change user agent
    chrome_options.add_argument(f'--user-agent={user_agent}')

    # save current/load previous session
    if save_session:
        chrome_options.add_argument('--user-data-dir=/home/seluser/userdata')

    # disable features not compatible with docker
    chrome_options.add_argument('--no-sandbox')

    # change view port
    chrome_options.add_argument('--start-maximized')

    # disable automation extension
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # configure browser settings
    chrome_options.add_experimental_option('prefs',  {
        'enable_do_not_track': True,                        # tell servers not to track us
        'webkit.webprefs.encrypted_media_enabled': False,   # disable protected content
    })

    driver = WebDriver(options=chrome_options, **options)

    # set timeout for driver operations
    driver.implicitly_wait(timeout)

    return driver

class Scraper:
    """
    Class for managing scraping of scripts in `/scrapper` directory.
    """

    DEFAULT_OPTIONS = {
        'command_executor': CHROME_URI,
    }

    def is_script(self, path: str) -> bool:
        """
        Validates if a script identified by `path` has been added with `add_script()`.

        Args:
            path (str): script to validate

        Returns:
            bool: `True` if script exists and `False` otherwise.
        """
        return \
            isinstance(path, str) \
            and path in self.scripts \
            and 'driver' in self.scripts[path] \
            and 'generator' in self.scripts[path] \
            and 'results' in self.scripts[path] \
            and 'future' in self.scripts[path]

    @staticmethod
    def run_script(generator: Generator[dict, None, None], results: list, driver: WebDriver):
        """
        Function passed to `ThreadExecutor.submit()`

        Args:
            generator (Generator[dict, None, None]): result of `Script.execute()`
            results (list): list to store results
            driver (WebDriver): selenium webdriver instance
        """
        try:
            # read
            for result in generator:
                results.append(result)

            # stop webdriver session
            if isinstance(driver, WebDriver):
                if driver.session_id:
                    driver.quit()

        except WebDriverException:
            pass

    def add_script(
        self,
        path: str,
        driver: WebDriver,
        script: Script,
        generator: Generator[dict, None, None],
    ):
        """
        Adds a new script to scrapper.

        Args:
            path (str): path to script in `/scrapper` directory
        """
        if not isinstance(path, str):
            raise TypeError('`path` must be a string')

        debug('Adding script ' + path)

        results = []
        future = self.executor.submit(self.run_script, generator, results, driver)

        # prevent race conditions
        time.sleep(4)

        self.scripts[path] = {
            'driver': driver,
            'script': script,
            'generator': generator,
            'results': results,
            'future': future,
        }

        debug('Running script ' + path)

    def get_script(self, path: str) -> Script:
        """
        Returns the `Script` instance created for the path.

        Args:
            path (str): path to script in `/scrapper` directory

        Returns:
            Script: `Script` instance created for path
        """
        if self.is_script(path) and isinstance(self.scripts[path]['script'], Script):
            return self.scripts[path]['script']

        return None

    def delete_script(self, path: str):
        """
        Deletes a script added with `add_script()`

        Args:
            path (str): path to script in `/scrapper` directory
        """
        if not self.is_script(path):
            return

        debug('Deleting script ' + path)

        # send stopsignal to script
        if isinstance(self.scripts[path]['generator'], Generator):
            self.scripts[path]['generator'].close()

        # stop webdriver session
        try:
            if isinstance(self.scripts[path]['driver'], WebDriver):
                if self.scripts[path]['driver'].session_id:
                    self.scripts[path]['driver'].quit()

                    # prevent race conditions
                    time.sleep(2)

        except WebDriverException:
            pass

        # cancel future
        if isinstance(self.scripts[path]['future'], Future):
            self.scripts[path]['future'].cancel()

        # delete script
        self.scripts[path] = {}

    def scrape (self, path: str, **kwargs) -> str:
        """
        Executes a script in the `/scrapper` directory.

        Args:
            path (str): path to script in `/scrapper` directory
            **kwargs (any): arguments forwarded to `Script.execute()`

        Returns:
            str: See `get_status()`
        """
        # delete previous script
        if self.is_script(path):
            self.delete_script(path)

        # create new script
        driver = create_driver(**self.options)
        script = create_script(path, driver, **self.options)
        generator = script.execute(**kwargs)

        self.add_script(path, driver, script, generator)

        return self.get_status(path)

    def get_status(self, path: str) -> str:
        """
        Returns the current status of script.

        Args:
            path (str): path to script in `/scrapper` directory

        Returns:
            str: `done` script has completed.
                 `invalid` invalid script.
                 `runnning` script is running.
                 `stopped` script hasn't started
        """
        if not self.is_script(path):
            return 'stopped'

        if not isinstance(self.scripts[path]['future'], Future):
            return 'invalid'

        if self.scripts[path]['future'].done():
            return 'done'

        return 'running'

    def get_results(self, path: str) -> list:
        """
        Return the collected results of a script.

        Args:
            path (str): script to get results of

        Raises:
            KeyError: if script is not created first with `add_script()`

        Returns:
            list[dict]: results or an empty `[]` if no results have been collected
        """
        if not self.is_script(path):
            raise KeyError(f'Invalid script `{path}`')

        results = []

        # loop through results
        if isinstance(self.scripts[path]['results'], list):
            while len(self.scripts[path]['results']) > 0:
                # transfer to results
                result = self.scripts[path]['results'].pop()

                results.append(result)

        debug('Fetched results: ' + str(len(results)))

        return results

    def __init__(self, **kwargs) -> None:
        self.options = {**self.DEFAULT_OPTIONS, **kwargs}
        self.scripts = {}
        self.executor = ThreadPoolExecutor(16)

    def __del__(self):
        # clean up scripts
        for script in self.scripts:
            self.delete_script(script)

        # free up thread executor
        self.executor.shutdown()


def create_scraper(**kwargs) -> Scraper:
    """
    Factory function for `Scraper`.

    Args:
        **timeout (int): value sent to `driver.implicitly_wait`. Defaults to 10
        **user_agent (str): user Agent header. Default to `CHROME_USER_AGENT`
        **save_session (bool): if `True` then current session will be stored and loaded.
                               Default to `False`
        **kwargs (any): all extra arguments are forwarded to seleniums `Webdriver()`
                        constructor

    Returns:
        Scraper: an instance of `Scraper`
    """
    return Scraper(**kwargs)
