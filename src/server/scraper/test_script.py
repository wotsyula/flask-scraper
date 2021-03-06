#!/usr/bin/env python3
"""
Tests for `script` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import os
import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains

from .script import (
    validate_script,
    sanitize_script,
    load_script,
    create_script
)

from .scripts.mock import Script

INVALID_PATHS = [
    None,
    '',
    [],
    {},
]

VALID_PATHS = [
    'google',
    'google/search',
    'facebook',
    'facebook/user',
    'facebook/page',
]

def test_validate_script():

    for path in INVALID_PATHS:
        assert validate_script(path) is False \
            , 'Should return false if path not a string'

    for path in VALID_PATHS:
        assert validate_script(path) is True \
            , 'Return true for if path is valid'

def test_sanitize_script():
    for path in INVALID_PATHS:
        # Should raise an error if path is not a string
        with pytest.raises(TypeError):
            sanitize_script(path)

    # Should raise an error if path contains full stop (.)
    with pytest.raises(TypeError):
        sanitize_script("abc.def")

    for number in range(0,10):
        # Should raise an error if path contains a number (0-9)
        with pytest.raises(TypeError):
            sanitize_script(f'abc{number}def')

    for path in VALID_PATHS:
        assert isinstance(sanitize_script(path), str) \
            , 'Should return string'

def test_load_script():
    # Should raise an error for non existent modules
    with pytest.raises(Exception):
        load_script('__non_existent_module__')

    mod = load_script('mock')

    assert hasattr(mod, 'Script') \
        , 'Should return a Script module'

class TestScript:
    @pytest.fixture
    def script(self, driver):
        return Script(driver)

    def test_referer(self, script):
        pass

    def test_sleep(self, script):
        prev_time = round(time.time() * 1000)

        script.sleep()

        curr_time = round(time.time() * 1000)

        assert curr_time - prev_time >= 300 \
            , 'It should halt execution'

        prev_time = round(time.time() * 1000)

        script.sleep(5)

        curr_time = round(time.time() * 1000)

        assert curr_time - prev_time >= 1500 \
            , 'It should halt execution multiplied by multiplier'

    def test_user_agent(self, script: Script):
        assert isinstance(script.user_agent, str) \
            , 'Should return a string'

    def test_cookies(self, script: Script):
        script.driver.get('https://httpbin.org/cookies/set?foo=1&bar=2')

        assert script.cookies == {'foo': '1', 'bar': '2'} \
            , 'Should return cookies'

    def test_page(self, script: Script):
        assert isinstance(script.page, int) \
            , 'Should return a number'

    def test_xpath(self, script: Script):
        pass

    def test_exists(self, script: Script):
        pass

    def test_click(self, script: Script):
        pass

    def test_send_keys(self, script: Script):
        pass

    def test_move_to(self, script: Script):
        script.driver.get('https://schema.org/LocalBusiness')

        script.move_to('//tr[@class="supertype"][3]')
        assert script.driver.execute_script('return window.scrollY') > 200 \
            , 'Should scroll to object'

        script.move_to('//tr[@class="supertype"][4]')
        assert script.driver.execute_script('return window.scrollY') > 400 \
            , 'Should scroll to object'

        script.move_to('//a[@href="/Organization"]')
        ActionChains(script.driver).click().perform()
        time.sleep(10)

        assert script.driver.current_url == 'https://schema.org/Organization' \
            , 'Should allow clicking of object using ActionChains'

    def test_scroll_to_bottom(self, script: Script):
        script.driver.get('https://worlds-highest-website.com')
        script.scroll_to_bottom()

        assert script.driver.execute_script('return window.scrollY') > 1000 \
            , 'Should scroll to bottom of page'

    def test_download(self, script: Script):
        script.driver.get('https://example.com')
        script.download('https://example.com/index.htm')

        assert os.path.isfile('index.htm') \
            , 'Should download a file'

        os.remove('index.htm')

    def test_is_recaptcha(self, script: Script):
        script.driver.get('http://example.com')

        assert not script.is_recaptcha() \
            , 'Should return `false` if no recaptcha field is present'

        script.driver.get('https://www.google.com/recaptcha/api2/demo')

        assert script.is_recaptcha() \
            , 'Should return `true` if recaptcha field is present'

    @pytest.mark.xfail
    def test_audio_to_speech(self, script: Script):
        expected = 'Okay we\'re trying this for a second time to test the ' \
                 + 'ability to upload and MP 3 files hopefully this will work.'
        test = script.audio_to_text(
            os.path.join(os.path.dirname(__file__), 'test.mp3')
        )

        assert test == expected \
            , 'Should return converted text'

    @pytest.mark.skip(reason="must be tested manually")
    def test_solve_recaptcha(self, script: Script):
        # go to test form
        # script.driver.get('https://recaptcha-demo.appspot.com/recaptcha-v2-invisible.php')

        # if script.is_recaptcha():
        #     # solve capcha
        #     script.solve_recaptcha()

        #     # submit / confirm
        #     script.click('//*[@type="submit"]')
        #     script.xpath('//*[text() = "Success!"]')

        # go to test form
        script.driver.get('https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php')

        if script.is_recaptcha():
            # solve capcha
            script.solve_recaptcha()

            # submit / confirm
            script.click('//*[@type="submit"]')
            assert script.xpath('//*[text() = "Success!"]')

        # # go to test form
        # script.driver.get('https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php')

        # if script.is_recaptcha():
        #     # solve capcha
        #     script.solve_recaptcha()

        #     # submit / confirm
        #     script.click('//*[@type="submit"]')
        #     script.xpath('//*[text() = "Success!"]')


def test_create_script(driver):
    # Should throw an error if module does not have 'Script' property
    with pytest.raises(KeyError):
        create_script('mockerror', driver)

    assert isinstance(create_script('mock', driver), Script) \
        , 'Should create a `Script` object'
