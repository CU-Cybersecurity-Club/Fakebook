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
Helper functions
"""


def generate_random_password(length):
    characters = string.ascii_uppercase + string.digits
    random_string = "".join(random.SystemRandom().choices(characters, k=length))
    return random_string
