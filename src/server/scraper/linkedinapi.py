#!/usr/bin/env python3
"""
Provides wrapper for Linkedin API using Selenium `WebDriver`
"""
import json
import logging
import random
import time
from typing import Dict

import requests
from requests.models import Response
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Remote as WebDriver
from selenium.webdriver.common.by import By

URL = 'https://www.linkedin.com/home'
API_BASE = 'https://www.linkedin.com/voyager/api/'


class LinkedInAPI():
    """
    Wraps LinkedIn API requests to a Selenium `WebDriver` instance

    Args:
        driver (WebDriver): `WebDriver` isntance

    Raises:
        TypeError: if `driver` is not an instance of `WebDriver`
        TypeError: if `driver` session is not logged in
    """

    @staticmethod
    def is_logged_in(driver: WebDriver) -> bool:
        """
        Checks if `driver` is logged in to LinkedIn website.

        Args:
            driver (WebDriver): `WebDriver` isntance

        Returns:
            bool: `True` if logged in and `False` otherwise
        """
        # navigate to LinkedIn
        if not 'linkedin.com' in driver.current_url:
            driver.get(URL)

        try:
            # check for navbar
            if driver.find_element(By.XPATH, '//ul[contains(@class, "nav")]'):
                return True

        except (TimeoutException, NoSuchElementException):
            pass

        return False

    @staticmethod
    def get_headers(driver: WebDriver) -> Dict[str, str]:
        """
        Retrieves headers from `WebDriver` instance to forward to `requests.session`.

        Args:
            driver (WebDriver): `WebDriver` isntance

        Returns:
            Dict[str, str]: headers to forward to `Session.headers`
        """
        # navigate to LinkedIn
        if not 'linkedin.com' in driver.current_url:
            driver.get(URL)

        # loop through logs
        headers = {}

        for raw_event in driver.get_log('performance'):
            event = json.loads(raw_event['message'])['message']

            # filter out requests
            if 'Network.requestWillBeSent' not in event['method']:
                continue

            # filter out api calls
            if \
                'request' not in event['params'] \
                or '/voyager/api' not in event['params']['request']['url'] \
                or 'content-type' in event['params']['request']['headers'] \
                or 'x-li-deco-include-micro-schema' in event['params']['request']['headers'] \
                or 'x-li-prefetch' in event['params']['request']['headers'] \
            :
                continue

            # parse headers
            headers.update(event['params']['request']['headers'])

        return headers

    @staticmethod
    def get_cookies(driver: WebDriver) -> Dict[str, str]:
        """
        Retrieves headers from `WebDriver` instance to forward to `requests.session`.

        Args:
            driver (WebDriver): `WebDriver` isntance

        Returns:
            Dict[str, str]: headers to forward to `Session.cookies`
        """
        # navigate to LinkedIn
        if not 'linkedin.com' in driver.current_url:
            driver.get(URL)

        # loop through cookies
        cookies = requests.sessions.RequestsCookieJar()

        for cookie in driver.get_cookies():
            cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie['domain'],
                path=cookie['path'],
                secure=cookie['secure'],
            )

        return cookies

    @staticmethod
    def sanitize_path(path: str) -> str:
        """
        Formats path passed to `call()`.

        Args:
            path (str): path to voyager api

        Returns:
            str: sanitized path
        """
        return str(path).replace('\\', '/').lstrip('/')

    def call(self, path: str, **kwargs) -> Response:
        """
        Makes call to LinkedIn API.

        Args:
            path (str): path to voyager api
            **kwargs (any): arguments forwarded to `Session.get()` / `Session.post()`

        Returns:
            bool: [description]
        """
        url = API_BASE + self.sanitize_path(path)

        self.logger.debug('Making API call to: %s', url)
        time.sleep(random.randint(10, 30) / 10)

        # if 'data' in kwargs:
        #     response = self.session.post(url, **kwargs)
        # else:
        response = self.session.get(url, **kwargs)

        if response.status_code != 200:
            self.logger.debug(
                'Invalid response: %s',
                response.status_code,
                extra=response.json(),
            )

        return response

    def get_profile(self, profile_id: str) -> Dict[str, any]:
        """
        Queries LinkedIn API for a profile

        Args:
            profile_id (str): LinkedIn id of profile to retrieve

        Returns:
            Profile: returns a JSON object
        """
        response = self.call(f'/identity/profiles/{profile_id}/profileView')

        return response.json()

    def __init__(self, driver: WebDriver) -> None:
        if not isinstance(driver, WebDriver):
            raise TypeError('`driver` must be an instance of `WebDriver`')

        if not self.is_logged_in(driver):
            raise TypeError('`driver` must be logged in already')

        self.logger = logging.Logger(__file__)
        self.session = requests.session()

        self.session.cookies.update(self.get_cookies(driver))
        self.session.headers.update(self.get_headers(driver))


def create_linkedinapi(driver: WebDriver) -> LinkedInAPI:
    """
    Creates a `LinkedInAPI` instance.

    Args:
        driver (WebDriver): `WebDriver` isntance

    Raises:
        TypeError: if `driver` is not an instance of `WebDriver`
        TypeError: if `driver` session is not logged in

    Returns:
        LinkedInAPI: instance of `LinkedInAPI`
    """
    return LinkedInAPI(driver)
