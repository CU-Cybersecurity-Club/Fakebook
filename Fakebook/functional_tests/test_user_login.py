"""
Tests to determine whether users can sign up, log in, and log out of the
site correctly.
"""

from .base import FunctionalTest


class UserLoginTests(FunctionalTest):
    def test_new_user_can_register(self):
        self.browser.get(self.live_server_url)
        self.assertEqual("Fakebook - Cybersecurity Club", self.browser.title)

        button = self.browser.find_element_by_id("signup-button")
        button.click()

        username_box = self.browser.find_element_by_name("username")
        password_box = self.browser.find_element_by_name("password")
        repassword_box = self.browser.find_element_by_name("repassword")

        self.assertEqual(username_box.get_attribute("placeholder"), "Username")
        self.assertEqual(password_box.get_attribute("placeholder"), "Password")
        self.assertEqual(
            repassword_box.get_attribute("placeholder"), "Re-enter password"
        )
        self.assertEqual(password_box.get_attribute("type"), "password")
        self.assertEqual(repassword_box.get_attribute("type"), "password")

        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        repassword_box.send_keys(self.password)

        button = self.browser.find_element_by_name("signup-submit-button")
        button.click()