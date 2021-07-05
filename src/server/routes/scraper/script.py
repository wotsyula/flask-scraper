#!/usr/bin/env python3
"""
Describes functions and classes for managing `Script` objects.
"""
import importlib
import os
import random
import re
import time

from abc import ABC, abstractmethod
from typing import Generator
from urllib.parse import urlparse

import requests
from selenium.common.exceptions import (
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import wait, expected_conditions as EC

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPTS = []

for directory in os.listdir(SCRIPT_DIR):
    abs_directory = os.path.join(SCRIPT_DIR, directory)

    if os.path.isdir(abs_directory):
        for script in os.listdir(abs_directory):
            if re.match('^[a-z]+.py$', script) is not None:
                SCRIPTS.append(directory + '/' + script[:-3])


def validate_script(path: str) -> bool:
    """
    Validates a script path from scraper directory.

    Args:
        path (str): path to validate

    Returns:
        bool: `True` if valid and `False` otherwise.
    """
    return isinstance(path, str) and len(path) > 0


def sanitize_script(path: str) -> str:
    """
    Validates and sanitizes a script path from scraper directory
    and returns it's python module name.

    Args:
        path (str): path to sanitize

    Raises:
        TypeError: If path is not an non-empty string
        TypeError: If path does not match regex `^([A-Za-z_]+/?)+$`

    Returns:
        str: module or `None` if unavailable
    """

    if validate_script(path) is not True:
        raise TypeError(f'path must be a non empty string ({path})')

    module = re.search(r'^([A-Za-z_]+/?)+$', path)

    if isinstance(module, re.Match) is not True:
        raise TypeError(f'invalid path {path})')

    module = '..' + module.group().rstrip('/').replace('/', '.')

    return module


def load_script(path) -> any:
    """
    Validates and sanitizes a script path from scraper directory
    and returns it's python module.

    Args:
        path ([type]): path to script

    Returns:
        any: module if successfull and `None` if not
    """
    module = sanitize_script(path)

    if module:
        module = importlib.import_module(module, __name__)

    return module


class Script (ABC):
    # pylint: disable=too-few-public-methods
    """
    Abstract class that all scripts inherit from.

    Args:
        driver (selenium.webdriver.remote.webdriver.Webdriver): driver to use for script

    Raises:
        TypeError: if driver is not an instance of Webdriver
    """
    DEFAULT_OPTIONS = {}

    @staticmethod
    def sleep(multiplier = 1):
        """
        Sleeps a random ammount of milliseconds (100-2,000) * `multiplier`

        Args:
            multiplier (int, optional): Multiplier of random milliseconds. Defaults to 1.

        Raises:
            TypeError: if not multiplier > 1
        """
        if not isinstance(multiplier, int) or multiplier < 1:
            raise TypeError('multiplier should be an number larger than 0')

        # Get duration to wait in milliseconds
        duration = multiplier * random.randint(300, 600) / 1000

        time.sleep(duration)


    def user_agent(self) -> str:
        """
        Returns the current 'User-Agent' header of script.

        Returns:
            str: `navigator.userAgent`
        """
        return self.driver.execute_script('return navigator.userAgent')

    def move_to(self, xpath: str):
        """
        Moves mouse to element found by xpath

        Args:
            xpath (str): XPath of element to move to
        """
        ActionChains(self.driver).move_to_element_with_offset(
            self.driver.find_element_by_xpath(xpath),
            random.randint(3, 8),
            random.randint(3, 8),

        ).perform()

    def xpath(self, xpath: str) -> WebElement:
        """
        Returns element found at XPath

        Args:
            xpath (str): XPath of element to find
        """
        # wait for element to become available
        element_exists = EC.presence_of_element_located((By.XPATH, xpath))

        return wait.WebDriverWait(self.driver, 30).until(element_exists)


    def click(self, xpath: str) -> None:
        """
        Clicks an element

        Args:
            xpath (str): XPath of element to click
        """
        self.move_to(xpath)

        element_clickable = EC.element_to_be_clickable((By.XPATH, xpath))

        wait.WebDriverWait(self.driver, 30).until(element_clickable)

        ActionChains(self.driver).click().perform()

        self.sleep(2)

    def send_keys(self, xpath: str, keys: str, click = False) -> WebElement:
        """
        Sends keystrokes to an element

        Args:
            xpath (str): XPath of element to click
            click (bool, optional): If `True` will click on element before sending keys.
                                    Defaults to False.
        """
        # click element
        if click:
            self.click(xpath)

        # enter characters with delay between keystrokes
        element_exists = EC.presence_of_element_located((By.XPATH, xpath))
        driver_wait = wait.WebDriverWait(self.driver, 10)

        driver_wait.until(element_exists).clear()

        for char in keys:
            driver_wait.until(element_exists).send_keys(char)
            time.sleep(random.randint(100,400) / 1000)


    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the current page.
        """
        # scroll down
        curr_x = 0
        count = 0

        while(
            count < 10
            and self.driver.execute_script(
                'return document.body.scrollHeight - window.scrollY',
            ) > 1100
        ):
            # move mouse
            if curr_x > 200:
                delta_x = random.randint(-5, -1)
            elif curr_x < 100:
                delta_x = random.randint(1, 5)
            else:
                delta_x = random.randint(-3, 3)

            curr_x += delta_x
            count += 1

            try:
                ActionChains(self.driver).move_by_offset(delta_x, 0).perform()
            except MoveTargetOutOfBoundsException:
                pass

            # scroll down
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            self.sleep(2)

        # go to bottom of page
        self.driver.execute_script(
            'window.scrollTo({left: 0, top: document.body.scrollHeight, behaviour: "smooth"});'
        )
        self.sleep(1)

    def download(self, url: str) -> str:
        """
        Downloads a file from the internet.

        Args:
            url (str): url of file to download

        Returns:
            str: returns the path to the downloaded file
        """
        # fetch url into file
        user_agent = self.driver.execute_script(
            "return navigator.userAgent;",
        )

        response = requests.get(
            url,
            headers = {
                'User-Agent': user_agent,
                'Referer': self.driver.current_url,
            },
            stream = True,
        )

        filename = os.path.abspath(
            os.path.join(
                'Downloads/',
                os.path.basename(urlparse(url).path)
            )
        )

        with open(filename, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

        return filename


    def is_recaptcha(self):
        """
        Checks for Google `ReCaptcha` input.
        See: https://www.google.com/recaptcha/about/

        Returns:
            bool: `True` if found and `False` otherwise
        """

        try:
            element_exists = EC.presence_of_element_located((
                By.XPATH,
                '//iframe[contains(@src, "google.com/recaptcha")]',
            ))

            wait.WebDriverWait(self.driver, 4).until(element_exists)

            return True

        except (NoSuchElementException, TimeoutException):
            pass

        return False


    def audio_to_text(self, path: str) -> str:
        """
        Converts audio file to text.

        Args:
            path (str): path to mp3 or mp4 file

        Returns:
            str: the converted text or `None`
        """
        # open new window
        self.driver.execute_script('window.open("","_blank");')
        self.driver.switch_to.window(self.driver.window_handles[1])

        # navigate to watson
        self.driver.get('https://speech-to-text-demo.ng.bluemix.net')

        # enter upload file
        self.xpath('//*[@accept]').send_keys(path)
        time.sleep(5)

        # grab text
        prev_text = None

        while True:
            # wait for processing
            time.sleep(5)

            text = self.xpath('//*[@data-id="Text"]').text.strip()

            if text == prev_text:
                break

            prev_text = text

        # close window
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return text


    def solve_recaptcha(self):
        """
        Attempts to solve Google `ReCaptcha` input.
        See: https://www.google.com/recaptcha/about/

        Returns:
            bool: `True` if successfull and `False` otherwise
        """
        try:
            # click captcha
            self.sleep(5)
            self.driver.switch_to.default_content()
            self.move_to('//*[contains(@class,"g-recaptcha")]')
            ActionChains(self.driver).click().perform()
        except (NoSuchElementException, TimeoutException):
            return False

        # enter audio check
        try:
            self.sleep(10)
            self.driver.switch_to.frame(
                self.driver.find_element_by_xpath('//iframe[contains(@title,"recaptcha")]')
            )
            self.move_to('//*[contains(@class, "rc-button-audio")]')
            ActionChains(self.driver).click().perform()
            self.sleep(10)

            # listen to audio
            for unused in range(random.randint(2,6)):
                ActionChains(self.driver).send_keys(Keys.SPACE).perform()
                time.sleep(random.randint(8000, 14000) / 1000)

        except (NoSuchElementException, TimeoutError):
            return True


        try:
            # fetch/translate audio
            url = self.xpath('//*[contains(@href, "mp3")]').get_attribute('href')
            path = self.download(url)
            text = self.audio_to_text(path)

            os.remove(path)

            # enter audio
            ActionChains(self.driver).send_keys(Keys.TAB).perform()

            for char in text + Keys.ENTER:
                time.sleep(random.randint(100,400) / 1000)
                ActionChains(self.driver).send_keys(char).perform()

            # check results
            time.sleep(5)

            error = self.driver.find_element_by_class_name('rc-audiochallenge-error-message')

            self.driver.switch_to.default_content()

            if error:
                return not error.text

            return True

        except (NoSuchElementException, TimeoutException):
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        return False


    @abstractmethod
    def execute(self, **kwargs) -> Generator[dict, None, None]:
        """
        Executes the script using `driver`.

        Args:
            **kwargs (dict[str, any]): Used to pass arguments to script


        Yields:
            Generator[dict, None, None]: Returns a list of `dict` values
        """

    def __init__(self, driver: WebDriver, **kwargs) -> None:

        if isinstance(driver, WebDriver) is not True:
            raise TypeError('driver should be an instance of Webdriver')

        super().__init__()

        self.options = {**self.DEFAULT_OPTIONS, **kwargs}
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = wait.WebDriverWait(self.driver, 30)
        self.current_page = 0

def create_script(path: str, driver: WebDriver, **kwargs) -> Script:
    """
    Creates a `Script` from scraper directory from module in path.

    Args:
        path (str): Relative position of script in scrapper directory
        driver (WebDriver): Selenium `Webdriver` instance

    Raises:
        Exception: [description]

    Returns:
        Script: [description]
    """
    mod = load_script(path)

    if hasattr(mod, "Script") is not True or isinstance(mod.Script, type) is not True:
        raise Exception(f'invalid module ({path})')

    return mod.Script(driver, **kwargs)
