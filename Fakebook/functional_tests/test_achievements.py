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

    pass
