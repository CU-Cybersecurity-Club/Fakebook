# CTF
It's a CTF!

web app with XSS vulnerabilities

## Testing
This repository contains some tests to ensure that the Fakebook app works correctly. To run these tests, simply run `pytest` from the root directory for the repo after downloading it and installing its dependencies.

* **Note**: in order to run the functional tests in `Fakebook/functional_tests`, you must have [geckodriver for Mozilla Firefox](https://github.com/mozilla/geckodriver) installed.

## TODO
* Testing
  * Add more functional tests to check that the achievements work correctly.
  * Add some functional tests for the chat. 
    * Note that Fakebook currently uses `socketio` to enable the chat, which only works if you start the app with the `socketio` value returned by `create_app()` in `Fakebook/app.py`. On the other hand, `flask_testing` (which is being used to run functional tests) can only start an app of type `flask.Flask`.
    * As a result, there is currently no way to run functional tests for the chat on Fakebook. We might need to convert the chat to pure Flask before than can be done.
  * Enable functional tests against a staging server.
* Sandboxing
  * Currently it's possible to inject code into other users' sessions using the (intentional) XSS vulnerabilities, which we probably don't want to be possible by default. Instead, we could separate the app into two pieces, "sandboxed" and "warzone". In the former, users can play with the app without worrying about interference from other users. In the latter, every user runs the same instance of the app.
* General
  * Add more achievements.
  * Add deployment automation scripts with Ansible that could be used to easily get this running on a remote server.
    * Should be easy to do (I already have some scripts that could be easily transferred over to this project), but it's not high-priority.
    * Put the application behind a Gunicorn server and an Nginx proxy.
* Miscellaneous
  * Create some Selenium bots to act as fake users that players can attack within their sessions.
    * We could get players to try and steal the bots' cookies to log in as them.
