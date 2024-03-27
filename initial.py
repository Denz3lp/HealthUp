"""
This document initializes and launches the database (connection) and
regulates user authentication progress and guidance.
It imports the library 'questionary' as the Command Line Interface (CLI) that guides the user through the program
as well as checks the user input. For user authentication (register and login) it additionally performs password check.
It imports User.py to get accesses to the UserClass.
Following libraries are used: questionary, sqlite3 and hashlib.
"""
import questionary
import sqlite3
import hashlib
import User

# Database launch
# generates 3 tables: User (user data information); Habit( all habit-related data)
# and Progress (connects habit-related progress with User)

def start_database():
    """
    Launch of the database if it not already exists.

    The database consists of three tables:
    * users --> for all user data
    * habits --> for all habits across all users
    * progress --> for all progress data across users
    """
    from os.path import join, dirname, abspath
    db_path = join(dirname(abspath(__file__)), 'healthup.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username text PRIMARY KEY,
                    password text,
                    firstname text,
                    lastname text
                    )""")

        c.execute("""CREATE TABLE IF NOT EXISTS habits (
                      habit_name TEXT PRIMARY KEY,
                      owner TEXT NOT NULL, 
                      periodicity TEXT NOT NULL,
                      datetime_creation DATETIME NOT NULL,
                      FOREIGN KEY(owner) REFERENCES users(username)
                      )""" )

        c.execute("""CREATE TABLE IF NOT EXISTS progress (
                  habit_name text,
                  periodicity text, 
                  owner text, 
                  datetime_completion datetime
                  )""")
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Following part is for user set up
# User have to register by entering Username, password, first and lastname (data is stored in db)
# User can login, username and password are checked

def register_user():
    """
     Deals with the User registration.

    User is asked to enter a username and password and their first and last name.
    The input is limited to letters except for Username and password (allowed to contain numbers).
    The user is created and the data is saved in the database.
    The username is the primary key and can only exist once. If the username already exists, the user is asked to choose another one.
    """
    username = questionary.text("Choose a username.",
                                  validate=lambda text: True if len(text)>0 and text.isalnum()
                                  else "Please enter a correct value. "
                                       "A Username can contain numbers and letters").ask()
    password = questionary.password( "Enter a password.",
                                      validate=lambda text: True if len(text)>= 8 and text.isalnum()
                                      else "Your password must be at least 8 characters long and can "
                                           "contain upper and lower case letters and numbers.").ask()
    firstname = questionary.text("What's your first name? ",
                                   validate=lambda text: True if len(text)>0 and text.isalpha()
                                   else "Please enter a correct value. "
                                        "Your name should only contain upper and lowercase letters.").ask()
    lastname = questionary.text("Please enter your last name. ",
                                  validate=lambda text: True if len(text)>0 and text.isalpha()
                                  else "Please enter a correct value. "
                                       "Your name should only contain upper and lowercase letters.").ask()
    # using hashlib to hash password
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # variable to initially collect user information but further check redundancy
    new_user = User.UserClass(username, password, firstname, lastname)
    user = get_user(username)
    if user:
        print("\nThis username already exists. Try again!\n")
        register_user()

    else:
        new_user.store_in_db()
        print("\nRegistration successful!\n")

# function to get the user ( if its exits)
def get_user(username):
    """
    function that interacts with the db to check if a given username exists in the 'users' table.
    If the user exists, it returns a user object containing the user's details; otherwise, it returns None.

    Parameters
    ----------
    :param username: str
        Assigned to the function by register_user() or login().
    """
    from os.path import join, dirname, abspath
    db_path = join(dirname(abspath(__file__)), 'healthup.db')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    list_of_users = cur.fetchall()

    if len(list_of_users) > 0:
        username, password, firstname, lastname = list_of_users[0]
        user = User.UserClass( username, password, firstname, lastname)
        return user
    else:
        return None

# function to regulate login of user.
def login():
    """
    Function that manages the login of a user.User is asked for username and password.
    It is checked whether the username exists. If yes, the entered password is checked.
    If the login is successful, it returns an instance of UserClass.
    Otherwise, the user is redirected to registration or given a chance to try again.

    Returns
    -------
    :return: UserClass instance for the logged-in user or None
    """
    while True:
        user_name = questionary.text("Enter your username: ").ask()
        user = get_user(user_name)

        if user:
            if check_password(user.password):
                return user
            else:
                print("\nIncorrect password. Please try again.\n")
        else:
            print("\nUsername not found.\n")
            choice = questionary.select("Choose an option:", choices=["Try Again", "Go to Register"]).ask()
            if choice == "Go to Register":
                return register_user()

# Password check, checks if the entered password matches those of the corresponding User Password.
def check_password(password):
    """
    Entered password by the user is checked with the password in the database.
    The user has 5 attempts to enter the correct password.

    :param password: str
        The correct password hash, to be compared with the user input.
    """
    attempt_limit = 5
    attempts = 0
    password_input = questionary.password("Enter your password: ").ask()

    while attempts < attempt_limit:
        password_input = hashlib.sha256(password_input.encode('utf-8')).hexdigest()

        if password_input == password:
            print("\nLogin successful!\n")
            return True

        attempts += 1
        if attempts < attempt_limit:
            print(f"\nPassword incorrect. You have {attempt_limit - attempts} attempts left. Try again!\n")
        else:
            print("\nYou have exceeded the maximum number of attempts.\n")
            break  # Exit the loop if the attempt limit is reached




