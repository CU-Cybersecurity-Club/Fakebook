from Fakebook import create_app, settings
from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.parse import quote
import dotenv
import os
import random
import sqlite3 as sql
import string

random.seed(0)

FUNCTIONAL_TESTS_DATABASE = "test.db"
settings["DATABASE"] = FUNCTIONAL_TESTS_DATABASE

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
        app.config.update(LIVESERVER_PORT=0)
        return app

    def setUp(self):
        self.browser = webdriver.Firefox()
        dotenv.load_dotenv()
        if "STAGING_SERVER" in os.environ:
            # Currently unused; will be useful for functional testing on a
            # staging server.
            self.live_server_url = "https://" + os.environ["STAGING_SERVER"]

            # Authenticate for staging server
            username = quote(os.environ["STAGING_SERVER_USERNAME"])
            password = quote(os.environ["STAGING_SERVER_PASSWORD"])
            url = "https://%s:%s@%s" % (username, password, staging_server)
            self.browser.get(url)
        else:
            self.live_server_url = self.get_server_url()

        # Create a test username and password
        self.email_address = "alice@example.com"
        self.username = "Alice"
        self.password = generate_random_password(32)

        # Reset the database
        with sql.connect(FUNCTIONAL_TESTS_DATABASE) as db:
            cur = db.cursor()
            cur.execute(
                "select 'drop table' || name || ';' from sqlite_master where type = 'table';"
            )
            with open(os.path.join("config", "default_database"), "r") as f:
                for cmd in f.readlines():
                    cur.execute(cmd)
            db.commit()

    def tearDown(self):
        self.browser.quit()

    """
    Helper functions for the FunctionalTest base class
    """

    def register_user(self, username, password):
        """
        Register a new user to the site
        """
        self.browser.get(self.get_server_url())
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
