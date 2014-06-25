from functools import wraps

from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash

from models import User
from database import db_session


"""In a real world application, we obviously can't use such a simple
authentication system, but for a tiny project like this, using a 3rd party
library (like Flask-Login) would be an overkill. A sufficient solution for our
small app is to use Werkzeug security functions to hash passwords. Since
Werkzeug is shipped with Flask, we're not installing external tools for that.
Anyway, relying on another authentication library would be straightforward if
we decided we want that.
"""


def requires_auth(f):
    """A simple decorator that checks if the user is logged in.

    If the user is logged in, the decorated function excutes normally.
    Otherwise, the decorated function is aborted with a 401 Unauthorized code.
    """
    @wraps(f)
    def login_needed(*args, **kwargs):
        if 'logged_in' not in session:
            abort(401)  # Unauthorized
        return f(*args, **kwargs)
    return login_needed


def check_user(user_name):
    """Returns the id of the user if user_name exists, or -1 otherwise.

    Args:
        user_name (str): The username to check.

    Returns:
        int.  The user id or -1:
            -1 -- User not found.
            Any other int -- the id of the user.
    """
    user_query = User.query.filter(User.username == user_name)
    if user_query.count() == 1:
        return user_query.first().id
    return -1


def check_account(user_name, password_hash):
    """Returns the id of the user if the provided credentials are correct,
        or -1 otherwise.

    Args:
        user_name (str): The username to check.
        password_hash (str): The password hash to check after we check whether
            user_name exists.

    Returns:
        int. The user id or -1:
            -1 -- The credentials are not accepted because either user_name or
                password_hash is not correct.
            Any other int -- The credentials are accepted. user_name and
                password_hash match an existing user account.
    """
    user_id = check_user(user_name)
    if user_id != -1 and check_password_hash(User.query.get(user_id).password,
                                             password_hash):
        return user_id
    return -1


def register_user(user_name, password):
    """Registers a new user account using the provided credentials.

    Args:
        user_name (str): The username to register.
        password_hash (str): The password used to generate the hash which will
                             be stored in the databse.

    Returns:
        bool.  Indicates if the registration was successful:
            True -- Registration was successful.
            False -- Either the supplied user_name already exists or an error
                     has occured.
    """
    if check_user(user_name) == -1:
        try:
            new_user = User(user_name, generate_password_hash(password))
            db_session.add(new_user)
            db_session.commit()
            return True
        except:
            pass
    return False
