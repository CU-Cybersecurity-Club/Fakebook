from .base import FunctionalTest, generate_random_password


class UserLoginTests(FunctionalTest):
    """
    Tests to determine whether users can sign up, log in, and log out of the
    site correctly.
    """

    def test_new_user_can_register(self):
        # Alice has heard about this hip, new CTF challenge from the cool kids in
        # the Cybersecurity Club, and decides to check it out.
        self.browser.get(self.get_server_url())
        self.assertEqual("Fakebook - Cybersecurity Club", self.browser.title)

        # Having never visited before, she clicks the signup button
        button = self.browser.find_element_by_id("signup-button")
        self.assertEqual(button.text, "Create Account")
        button.click()

        # She creates a new account by entering her username and password on the
        # signup page, where prompted.
        username_box = self.browser.find_element_by_name("username")
        password_box = self.browser.find_element_by_name("password")
        repassword_box = self.browser.find_element_by_name("repassword")

        self.assertEqual(username_box.get_attribute("placeholder"), "Username")
        self.assertEqual(password_box.get_attribute("placeholder"), "Password")
        self.assertEqual(
            repassword_box.get_attribute("placeholder"), "Re-enter password"
        )
        self.assertEqual(username_box.get_attribute("type"), "text")
        self.assertEqual(password_box.get_attribute("type"), "password")
        self.assertEqual(repassword_box.get_attribute("type"), "password")

        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        repassword_box.send_keys(self.password)

        # She clicks the "Create" button to finish the signup process
        button = self.browser.find_element_by_name("signup-submit-button")
        self.assertEqual(button.get_attribute("value"), "Create")
        button.click()

        # Alice arrives at her homepage. She is given a unique token for her session.
        self.assertTrue(
            f"Welcome to the Fakebook beta, {self.username}!"
            in self.browser.page_source
        )
        cookies = self.browser.get_cookies()
        self.assertEqual(len(cookies), 1)
        self.assertEqual(cookies[0]["name"], "token")
        self.assertNotEqual(cookies[0]["value"].lower(), "None")

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
        self.assertEqual(self.browser.current_url, self.get_server_url() + "/login")
        self.assertTrue("Welcome to Fakebook beta!" in self.browser.page_source)

    def test_can_log_in_after_registering(self):
        # Alice registers herself with the site, then logs out.
        self.register_user(self.username, self.password)
        original_url = self.browser.current_url
        original_page_source = self.browser.page_source

        self.browser.find_element_by_id("logout").click()

        # She returns to the login page
        self.assertTrue("Welcome to Fakebook beta!" in self.browser.page_source)
        self.assertEqual(self.browser.current_url, self.get_server_url() + "/login")

        # She enters her credentials into the username and password boxes
        username_box = self.browser.find_element_by_name("username")
        password_box = self.browser.find_element_by_name("password")
        self.assertEqual(username_box.get_attribute("placeholder"), "Username")
        self.assertEqual(password_box.get_attribute("placeholder"), "Password")
        self.assertEqual(username_box.get_attribute("type"), "text")
        self.assertEqual(password_box.get_attribute("type"), "password")

        username_box.send_keys(self.username)
        password_box.send_keys(self.password)

        # She clicks the "Submit" button, and returns to her homepage.
        button = self.browser.find_element_by_name("submit-button")
        self.assertEqual(button.get_attribute("value"), "Submit")
        button.click()

        self.assertEqual(self.browser.page_source, original_page_source)
        self.assertEqual(self.browser.current_url, original_url)

    def test_cannot_log_in_with_incorrect_credentials(self):
        # Alice registers herself with the site, then logs out
        self.register_user(self.username, self.password)
        self.browser.find_element_by_id("logout").click()

        # Now Eve comes along, and tries to log in as Alice with incorrect credentials
        wrong_password = generate_random_password(32)
        self.browser.find_element_by_name("username").send_keys(self.username)
        self.browser.find_element_by_name("password").send_keys(wrong_password)
        self.browser.find_element_by_name("submit-button").click()

        # The site tells her that she used invalid credentials
        self.assertTrue("Invalid login!" in self.browser.page_source)
        cookies = self.browser.get_cookies()

        self.assertEqual(len(cookies), 1)
        self.assertEqual(cookies[0]["name"], "token")
        self.assertEqual(cookies[0]["value"], "None")
