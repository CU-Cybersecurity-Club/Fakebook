from .base import FunctionalTest


class AchievementTests(FunctionalTest):
    """
    Tests to determine that all of the achievements work correctly. Currently, the
    following achievements are available:

    1. _Create account_: participation trophy for figuring out how to make an account :)
    2. _Break server_: cause an internal error in the server.
    3. _Find login_: given for finding the login for the user nobodyknowsme
    4. _XSS alert_: given for injecting a JavaScript 'alert();' into a page.
    5. _Redirect page_: given for injecting JavaScript that redirects users to another page.
    6. _Password: Mel_: given for logging in as user Mel.
    7. _Stolen token_: given for logging in with the 'token' cookie of another player.
    8. _Find hidden path_: given for finding /hidden.
    """

    def test_create_account_achievement(self):
        # Alice visits the site, and enters her name to register for the CTF
        self.register_ctf_user(self.name)

        # Alice registers as a user to the site.
        self.register_user(self.username, self.password)
        self.browser.get(self.get_server_url() + "/scoreboard")

        # She visits the scoreboard. At the top of the scoreboard are column
        # headers for username, total score, and then one column per achievement.
        table = self.browser.find_element_by_tag_name("table")
        th = table.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        self.assertEqual(len(th), 10)
        self.assertEqual(th[0].text, "User")
        self.assertEqual(th[1].text, "Score")

        # Below, there is a table with all of the achievements of each user so far.
        # Alice looks at her row; it shows that she has points for registering
        # on the site.
        rows = table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        rows = [r for r in rows if self.name in r.text]
        self.assertEqual(len(rows), 1)

        cols = rows[0].find_elements_by_tag_name("td")

        # 1. The first column should show her name
        self.assertEqual(cols[0].text, self.name)

        # 2. The second column should show the number of points she has
        self.assertEqual(cols[1].text, "1")

        # 3. The third column should show that she has reached the first
        #   achievement
        self.assertEqual(cols[2].text, "✔")

        # The remaining columns should all be blank
        for c in cols[3:]:
            self.assertEqual(c.text, "")
