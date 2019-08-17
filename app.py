from Fakebook import app, socketio, settings

# achievements = {
#     'created-account': (1, 'Create account', 'Create your account!'),
#     'server-error': (2, 'Break server', 'Cause an internal server error.'),
#     'sql-error': (3, 'Discover query', 'Figure out the SQL query that the website uses to log you on. (Hint - sometimes poorly-written server errors are displayed to users)'),
#     'sql-login': (4, 'Blind SQL', 'Use SQL injection to log on as the first user in the database.'),
#     # 'divine-command': (3, 'Divine command', 'Requirements hidden'),
#     # 'rickrolled': (3, 'Rickrolled', 'Requirements hidden'),
#     'hit-by-alert': (5, 'XSS victim', 'Get hit by another player\'s XSS alert!'),
#     'sql-specific-login': (6, 'Targeted SQL', 'Use SQL injection to log on as a specific user.'),
#     'alert': (7, 'XSS alert', 'Use XSS to insert an alert.'),
#     'password-mel': (8, 'Password: Mel', 'Log in with Mel\'s password.'),
#     'password-catl0v3r': (9, 'Password: CATl0v3r', 'Log in with CATl0v3r\'s password.'),
#     'password-grace': (10, 'Password: Grace', 'Log in with Grace\'s password.'),
#     'password-admin': (11, 'Password: Admin', 'Log in with Admin\'s password.'),
#     'stolen-token': (12, 'Stolen token', 'Steal a session token from another user. (Hint - reading it over the network might be required)'),
# }
#
# players = {
#     'Alexander': ['alert', 'sql-login'],
#     'Mark': ['sql-login'],
# }


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=settings["PORT"])
