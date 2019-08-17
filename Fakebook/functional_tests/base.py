from Fakebook import create_app
from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.parse import quote
import dotenv
import os
import random
import string

FUNCTIONAL_TESTS_LIVESERVER_PORT = 8001

"""
Base class for functional tests
"""


class FunctionalTest(LiveServerTestCase):
    """
    Base class for creating functional tests for the Fakebook app
    """

    """
    Functions to comply with the LiveServerTestCase API
    """

    def create_app(self):
        app, sio = create_app(__name__)
        app.config.update(LIVESERVER_PORT=FUNCTIONAL_TESTS_LIVESERVER_PORT)
        return app

    def setUp(self):
        self.browser = webdriver.Firefox()
        dotenv.load_dotenv()
        if "STAGING_SERVER" in os.environ:
            self.live_server_url = "https://" + os.environ["STAGING_SERVER"]

            # Authenticate for staging server
            username = quote(os.environ["STAGING_SERVER_USERNAME"])
            password = quote(os.environ["STAGING_SERVER_PASSWORD"])
            url = "https://%s:%s@%s" % (username, password, staging_server)
            self.browser.get(url)
        else:
            # For local development purposes only
            self.live_server_url = (
                f"http://localhost:{FUNCTIONAL_TESTS_LIVESERVER_PORT}"
            )

        # Create a test username and password
        self.email_address = "alice@example.com"
        self.username = "Alice"
        self.password = generate_random_password(32)

    def tearDown(self):
        self.browser.quit()

    """
    Helper functions for the FunctionalTest base class
    """

    def register_user(self, username, password):
        """
        Register a new user to the site
        """
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("signup-button").click()

        self.browser.find_element_by_name("username").send_keys(self.username)
        self.browser.find_element_by_name("password").send_keys(self.password)
        self.browser.find_element_by_name("repassword").send_keys(self.password)

        self.browser.find_element_by_name("signup-submit-button").click()


"""
General helper functions
"""


def generate_random_password(length):
    characters = string.ascii_uppercase + string.digits
    random_string = "".join(random.SystemRandom().choices(characters, k=length))
    return random_string
