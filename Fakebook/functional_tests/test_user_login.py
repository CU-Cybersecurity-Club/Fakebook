from .base import FunctionalTest, generate_random_password


class UserLoginTests(FunctionalTest):
    """
    Tests to determine whether users can sign up, log in, and log out of the
    site correctly.
    """

    def test_new_user_can_register(self):
        self.browser.get(self.live_server_url)
        self.assertEqual("Fakebook - Cybersecurity Club", self.browser.title)

        button = self.browser.find_element_by_id("signup-button")
        self.assertEqual(button.text, "Create Account")
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

        self.browser.find_element_by_name("signup-submit-button").click()

        # TODO: Ensure that Alice arrives at the homepage
        self.assertTrue(
            f"Welcome to the Fakebook beta, {self.username}!"
            in self.browser.page_source
        )
        self.fail("TODO")

    def test_same_user_cannot_register_twice(self):
        """
        Once registered, a username should be unavailable
        """
        # Alice registers herself as a user for the site
        self.register_user(self.username, self.password)
        self.browser.find_element_by_id("logout").click()

        # Now Eve tries to register herself as Alice, using the same username
        # and password. The site tells her that the username has already been
        # taken.
        self.register_user(self.username, self.password)
        self.assertTrue(
            f"Username {self.username} already taken!" in self.browser.page_source
        )

        # Eve tries again, this time using a different password. The page once
        # again tells her the username is already taken. In the database, the
        # entry for the user does not change.
        self.register_user(self.username, generate_random_password(32))
        self.assertTrue(
            f"Username {self.username} already taken!" in self.browser.page_source
        )

        # TODO: ensure that the database has not changed
        self.fail("TODO")

    def test_user_can_logout(self):
        # Alice registers herself as a user for the site
        self.register_user(self.username, self.password)

        # Now she clicks the logout button to exit the site
        button = self.browser.find_element_by_id("logout")
        self.assertEqual(button.text, "Logout")
        button.click()

        # She should now be returned to the /login page
        self.assertEqual(self.browser.current_url, self.live_server_url + "/login")
        self.assertTrue("Welcome to Fakebook beta!" in self.browser.page_source)
