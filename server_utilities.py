from model import db, connect_to_db, User




def email_in_database(email):
    """Returns true if the given email is found in the Users table."""

    #count how many users in the database have the given email (should be 1 or 0)
    num_matched = (db.session.query(User)
                             .filter(User.email == email)
                             .count())

    #if there's a user with that email, return true; otherwise, return false
    if num_matched == 1:
        return True
    else:
        return False


def username_in_database(username):
    """Returns true if the given username is found in the Users table."""

    #count how many users in the database have the given username (should be 1 or 0)
    num_matched = (db.session.query(User)
                             .filter(User.username == username)
                             .count())

    #if there's a user with that username, return true; otherwise, return false
    if num_matched == 1:
        return True
    else:
        return False


def password_is_correct(credential, password):
    """Verifies that password is the correct one for user with given
       credential (either username or password). Returns true for a match."""

    #hash the password and make it a string, since that's how they're stored
    hashed_pw = str(hash(password))

    #the presence of an @ symbol means the credential is an email
    if "@" in credential:
        user = db.session.query(User).filter(User.email == credential).first()
    #otherwise, assume it's a username
    else:
        user = db.session.query(User).filter(User.username == credential).first()

    #it's possible the credential isn't in the database at all, in which case
    #user will be None; clearly, then, the password doesn't match, so return false
    if not user:
        return False

    #otherwise, we have a valid user, but we still don't know if the passwords match
    else:
        #return true if the passwords match, and false otherwise
        if hashed_pw == user.password:
            return True
        else:
            return False


def user_is_logged_in(**kwargs):
    """Takes a user_id, username, *or* email, and determines if the associated
       user (if any) is logged in.

       Note that 1) only one credential may be specified, and 2) if the
       given credential is bogus (not in the database), false is also
       returned."""

    #make sure exactly one of [user_id, username, email] was passed; raise
    #a TypeError otherwise
    num_args = len(kwargs)
    okay_keys = ["user_id", "username", "email"]
    passed_keys = kwargs.keys()
    if num_args == 0:
        raise TypeError("too few arguments; expected 1, got 0.")
    elif num_args > 1:
        error_msg = "too many arguments; expected 1, got {num}."
        raise TypeError(error_msg.format(num=num_args))
    elif len(passed_keys.intersection(okay_keys)) == 0:
        raise TypeError("expected user_id, username, or email keyword argument.")

    #now that we know we have exactly one (valid) keyword argument, get it
    credential_type, credential = kwargs.items()[0]

    #get the user_ids of the user associated with that credential (if any) and
    #the logged-in user (again, if any)
    user_id = (db.session.query(User.user_id)
                         .filter(getattr(User, credential_type) == credential)
                         .first())
    logged_in_user_id = session.get("logged_in_user_id")

    #if the user wasn't found, or isn't logged in, return false
    if (not user_id) or (user_id != logged_in_user_id):
        return False
    else:  #they match!
        return True


def table_record_object_to_dict(record_object):
    """Takes an object representing a record from the database and creates
       a dictionary out of its values (as strings)"""

    pass

    # record_dict = {}

    # #add each of the object's attributes, excluding dunder attributes
    # #(because we don't care about them) and the user_id (because we've
    #     #already got it)...
    #     for attr, value in self.__dict__.items():
    #         # print attr, type(attr)
    #         # print value, type(value)
    #         if attr.startswith(("_", "password")):

    #             #pop it from the dictionary