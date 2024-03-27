"""
This document contains the user class. It deals with all the important functions of the programme.
It can create and manage several users, and all functions always refer to the logged-in user.
This code part contains functions to manage the user profile, to create and manage user specific habits and
all functions around analysis.

It imports the libraries' questionary, sqlite, datetime and hashlib.
It further imports the habit.py document to be able to use the HabitClass.
"""
import questionary
import sqlite3
from datetime import datetime, timedelta
import hashlib
import habit


# THE USER CLASS.
class UserClass:
    """
    Attributes
    ----------
    username: str
        the username defined by the user
    password: str
        the password used by the user
    firstname: str
        the firstname of the user
    lastname: str
        the lastname of the user

    Methods
    -------
    store_in_db()
        stores the user data into the db
    update_profile()
        used to update user profile data (can change password, first and lastname)
    store_habit_in_db(new_habit)
        stores a new habit into the database
    get_habit(habit_name)
        retrieves a habit from the database and gets all its information
    choose_predefined_habit()
        user can choose from a list of predefined habits if they have no habits stored in the db yet
    create_habit()
        lets the user create a new habit
    delete_habit()
        lets the user delete any habit from the db
    update_habit()
        lets the user update certain elements from their habit (periodicity, category)
    show_all()
        shows all habits of the user
    show_monthly_habits()
        shows all monthly habits of the user
    show_weekly_habits()
        shows all weekly habits of the user
    show_daily_habits()
        shows all daily habits of the user
    is_completed()
        herewith the user can mark a habit as done
    get_habit_progress(habit_name, periodicity)
        retrieves the progress of a certain habit with a certain periodicity from the database
    streak_overview()
        displays all current streaks of all habits of the user
    streak_habit()
        displays the current streak for a specific habit
    longest_streak_overview()
        displays the longest streaks among all habits of the user
    longest_streak_habit()
        displays the longest streak for a specific habit
    compute_streak(habit_name)
        computes the current habit streak
    compute_longest_streak_habit(habit_name)
        computes the longest habit streak
    """

    # USER MANAGEMENT
    # INIT METHOD.
    def __init__(self, username, password, firstname, lastname):
        """
        Parameters
        ----------
        :param username: the username defined by the user
        :param password: the password used by the user
        :param firstname: the firstname
        :param lastname: the lastname
        """
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

        from os.path import join, dirname, abspath
        db_path = join(dirname(abspath(__file__)), 'healthup.db')

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    # User Data Storage.
    def store_in_db(self):
        """
        Stores the user data into the database.
        Function is used when first registering a user.
        """
        self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                         ( self.username, self.password, self.firstname, self.lastname))
        self.conn.commit()

    # registered User can update profile
    def update_profile(self):
        """
        Allows a registered user to update their first name, last name, or password.
        The user selects an element to update, provides the new value, and the update is saved in the database.
        Passwords must be at least 8 characters long and contain letters and numbers.
        """
        choices = ["first name", "last name", "password"]
        element = questionary.select("What do you want to update? ", choices=choices).ask()

        if element == "password":
            new_entry = questionary.password(
            "Enter a new password: ",
            validate=lambda text: True if len(text)>= 8 and text.isalnum() else
            "Password must be at least four characters long and contain letters and numbers."
            ).ask()
            new_entry = hashlib.sha256(new_entry.encode('utf-8')).hexdigest()
        else:
            new_entry = questionary.text(f"What should your {element} now be?").ask()

        column = 'firstname' if element == 'first name' else 'lastname' if element == 'last name' else 'password'
        self.cur.execute(f"UPDATE users SET {column} = '{new_entry}' WHERE username = '{self.username}';" )
        self.conn.commit()
        print (f"\nYou successfully updated your {element}.\n")

    # HABIT MANAGEMENT

    # stores habit into db
    def store_habit_in_db(self, new_habit):
        """
        Stores habit data into the database, if it does not exist already.
        """
        # Check if habit already exists
        self.cur.execute ("SELECT * FROM habits WHERE habit_name = ? AND owner = ?",
                           (new_habit.habit_name, new_habit.owner))
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO habits VALUES(?, ?, ?, ?)",
                               (new_habit.habit_name, new_habit.owner,
                                new_habit.periodicity, new_habit.datetime_creation))
            self.conn.commit()
        else:
            print (f"The habit '{new_habit.habit_name}' already exists for user '{new_habit.owner}'.")

    # db query do get the habit name
    def get_habit(self, habit_name):
        """
        Retrieves habit from db. If the habit_name exists for the given owner, it returns the habit. Otherwise, returns None.
        """
        self.cur.execute("SELECT * FROM habits WHERE habit_name = ? AND owner = ?",(habit_name, self.username))
        list_of_habits = self.cur.fetchall()

        if list_of_habits:
            habit_name, owner, periodicity, datetime_creation = list_of_habits[0]
            hab = habit.HabitClass(habit_name, owner, periodicity, datetime_creation)
            return hab

    # New User can choose from a set of predefined habits (directly after first login)
    def choose_predefined_habit(self):
        """
        Offers the user a choice to adopt habits from a predefined list. It checks each predefined habit and asks
        the user if they want to adopt it only if it's not already stored in the database.
        """
        print("Let's choose your habits:")
        predefined_habits = [
            {"name": "Sleep", "periodicity": "daily"},
            {"name": "Water", "periodicity": "daily"},
            {"name": "Swimming", "periodicity": "monthly"},
            {"name": "Running", "periodicity": "weekly"},
            {"name": "Gym", "periodicity": "monthly"}
        ]
        for hab in predefined_habits:
            existing_habit = self.get_habit(hab['name'])
            if not existing_habit:
                confirm = questionary.confirm(
                    f"Would you like to use the habit: {hab['name']} ({hab['periodicity']})?" ).ask()
                if confirm:
                    habit_name = hab['name']
                    owner = self.username
                    periodicity = hab['periodicity']
                    datetime_creation = datetime.now()

                    new_habit = habit.HabitClass(habit_name, owner, periodicity, datetime_creation)
                    self.store_habit_in_db(new_habit)
            else:
                return None
            self.conn.commit()

    # habit creation
    def create_habit(self):
        """
        User is asked questions that allows him to create a new Habit. Following attributes are passed:
        habit name(only letters allowed), Periodicity (daily, weekly, monthly).
        The assignment to the user = owner and the datetime_creation are created automatically.
        Subsequently, the get_habit(habit_name) method is used to check whether the habit already exists.
        function returns a new habit that is saved in the db (by calling store_habit_in_db(new_habit)).
        """
        habit_name = questionary.text("Type in the name of the habit: ",
                                            validate=lambda text: True if len (text) > 0 and text.isalpha()
                                            else "Please enter a correct value. "
                                                 "Your habit name should only contain letters.").ask()
        owner = self.username
        periodicity = questionary.select("choose the periodicity of the habit.",
                                               choices=[
                                                   "daily",
                                                   "weekly",
                                                   "monthly"]).ask()
        datetime_creation = datetime.now()

        new_habit = habit.HabitClass(habit_name, owner, periodicity, datetime_creation)
        existing_habit = self.get_habit(habit_name)
        if existing_habit:
            print("\nThis habit already exists. Try again!\n")
            return self.create_habit()
        else:
            self.store_habit_in_db(new_habit)
            print("\nWell done! You created a new habit. \n")

    # habit deletion
    def delete_habit(self):
        """
        Removes a habit from the database. User is asked to enter a habit name. The function checks
        by calling get_habit(habit_name) if the habit exists in the db. If it does not exist, it prints a statement.
        If it exists, it deletes the habit from the database and returns a success statement.
        """
        habit_name = questionary.text("Which habit do you want to delete? ",
                                validate=lambda text: True if len(text)>0 and text.isalpha()
                                else "Please enter a correct value.").ask()
        existing_habit =self.get_habit(habit_name)

        if existing_habit:
            self.cur.execute(f"DELETE FROM habits WHERE habit_name = '{habit_name}' AND owner = '{self.username}';")
            self.cur.fetchall()
            self.conn.commit()
            print(f"'{habit_name}' successfully deleted.")
        else:
            print("\nNo such habit in the database!\n")

    # update of habit details.
    def update_habit(self):
        """
        Updates the specified attribute of an existing habit.

        This method allows the user to update either the 'task' or 'periodicity' of a habit. The user is first prompted
        to enter the name of the habit they wish to change. If the habit exists, the user is then asked which attribute
        ('task' or 'periodicity') they want to update. After selecting the attribute, the user is prompted to enter the
        new value for that attribute. The method updates the habit in the db with the new value.
        """
        to_change = questionary.text("What habit do you want to change? ",
                                     validate=lambda text: True if len(text) > 0 and text.isalpha()
                                     else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(to_change)
        if existing_habit:
            element = questionary.select("do you want to change the periodicity? ",
                                           choices=["periodicity"]).ask()
            new_value = questionary.text(f"Enter new {element}: ").ask()
            self.cur.execute(f"UPDATE habits SET {element} = ? WHERE habit_name = ? AND owner = ?",
                               (new_value, to_change, self.username))
            self.conn.commit()
            print(f"\nYou successfully updated the {element} for your habit.\n")
        else:
            print("This habit is not in the database.")

    # ACTIVITY OVERVIEW.

    # DB query do get all habits or filtered by periodicity.
    def show_all(self):
        """
        Queries the db and returns a list of habits for the user.
        Can return all habits.
        Returns:
        list: A list of all habits.
        """
        self.cur.execute("SELECT habit_name FROM habits WHERE owner = '{}';".format(self.username))

        items = self.cur.fetchall()
        habits = [item[0] for item in items]

        print(habits)
        return habits

    # db query for all monthly habits
    def show_monthly_habits(self):
        """
        Queries the database and returns a list of the monthly habits.

        Returns
        -------
        :return: list
            returns a list of monthly habits
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE periodicity = 'monthly' AND owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # DB query for all weekly habits
    def show_weekly_habits(self):
        """
        Queries the database and returns a list of the weekly habits of the currently logged-in user.
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE periodicity = 'weekly' AND owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # DB query to display a list of daily habits
    def show_daily_habits(self):
        """
        Queries the database and returns a list of the daily habits of the currently logged-in user.
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE periodicity = 'daily' AND owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # Habit completion
    def is_completed(self):
        """
        A user can mark a task as done. Therefore, the user enters the habit name. When the habit exists in the db,
        the program sets the date and time of completion and saves the progress.
        The user is informed via print statement if they were successful with adding the progress.
        """
        to_complete = questionary.text("What habit do you want to mark as completed? ",
                                       validate=lambda text: True if len(text)>0 and text.isalpha()
                                       else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(to_complete)

        if existing_habit:
            datetime_completion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("INSERT INTO progress VALUES(?, ?, ?, ?)",
                             (existing_habit.habit_name, existing_habit.periodicity, self.username,
                              datetime_completion))
            self.conn.commit()
            print("Great! you made progress. Well done!")

        else:
            print("This habit does not exist.")

    # all saved progress for a certain habit
    def get_habit_progress(self, habit_name, periodicity):
        """
        Gets the date and time of completion of a specific habit from the database.

        Parameters
        ----------
       habit_name: int
       periodicity:
            int --> daily, monthly, weekly

        Returns
        -------
        :return:
            user_progress --> if there is any saved progress in the database
        """
        # Execute query
        self.cur.execute (
            "SELECT datetime_completion FROM progress WHERE owner = ? AND habit_name = ? AND periodicity = ?;",
            (self.username, habit_name, periodicity))
        user_progress = self.cur.fetchall ()
        return user_progress

    # STREAK ANALYSIS

    #for the user to see stats of all habits
    def streak_overview(self):
        """
        Shows the user a current streak overview of all their habits.
        """
        # for daily habits
        self.cur.execute(
            f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'daily';")
        daily_habits = self.cur.fetchall()
        for habit_info in daily_habits:
            habit_name = habit_info[0]
            daily_streak = self.compute_streak(habit_name,periodicity= 'daily')
            print(f"The current streak of {habit_name} is: ", daily_streak, " day(s)")

        # weekly habits
        self.cur.execute(
            f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'weekly';")
        weekly_habits = self.cur.fetchall()
        for habit_info in weekly_habits:
            habit_name = habit_info[0]
            weekly_streak = self.compute_streak(habit_name, periodicity= 'weekly')
            print(f"The current streak of {habit_name} is: ", weekly_streak, " week(s)")

        # monthly habits
        self.cur.execute(
                f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'monthly';")
        monthly_habits = self.cur.fetchall()
        for habit_info in monthly_habits:
            habit_name = habit_info[0]
            monthly_streak = self.compute_streak(habit_name, periodicity= 'monthly')
            print(f"The current streak of {habit_name} is: ", monthly_streak, " month(s)")
        return

    # function for user guidance to see stats of a chosen habit
    def streak_habit(self):
        """
        Returns the current streak of a specific habit.

        enter a habit name, when it exists, the function calls the functions
        compute_streaks according the periodicity.
        """
        selected_habit = questionary.select(
            "Choose a habit to see its streak:",
            choices=self.show_all()).ask()

        # Ensure that habit_name is a string, not a tuple
        habit_name = selected_habit[0] if isinstance (selected_habit, tuple) else selected_habit

        existing_habit = self.get_habit(habit_name)
        periodicity = existing_habit.periodicity

        if existing_habit:
            if periodicity == "daily":
                streak = self.compute_streak(habit_name, periodicity= 'daily')
                if streak is not None:
                    print(f" Awesome! your current {habit_name} streak is ", streak, " days!")
                else:
                    print("No daily Streaks for that.")

            elif periodicity == "weekly":
                streak = self.compute_streak(habit_name, periodicity= 'weekly')
                if streak is not None:
                    print(f"You completed {habit_name} in ",streak," weeks in a row, Great!")
                else:
                    print("No weekly Streaks for that.")
            else:
                streak = self.compute_streak(habit_name, periodicity= 'monthly')
                if streak is not None:
                    print(f" {habit_name} has currently this streak: ", streak, " months")
                else:
                    print("No monthly Streaks for that.")
        else:
            print("This habit does not exist.")

    # function for user guidance to see the longest streak
    def longest_streak_overview(self):
        """
        Shows the user their longest streak of all their habits sorted by periodicity.
        """
        # for daily habits
        self.cur.execute (
            f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'daily';" )
        daily_habits = self.cur.fetchall()
        daily_streaks = [(hab[0], self.compute_longest_streak_habit(hab[0], 'daily')) for hab in daily_habits]

        if daily_streaks:
            max_daily_streak = max(daily_streaks, key=lambda e: e[1])
            print(f"Your longest streak is {max_daily_streak[1]} day(s) for habit '{max_daily_streak[0]}'.")
        else:
            print("No streaks. Go make some progress.")
            return

        # Weekly habits
        self.cur.execute (
            f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'weekly';" )
        weekly_habits = self.cur.fetchall()
        weekly_streaks = [(hab[0], self.compute_longest_streak_habit(hab[0], 'weekly')) for hab in weekly_habits]
        if weekly_streaks:
            max_weekly_streak = max(weekly_streaks, key=lambda e: e[1])
            print (
                f"With {max_weekly_streak[1]} week(s) is habit '{max_weekly_streak[0]}' your longest running Habit. Well done!" )
        else:
            print ("No Streaks for weekly habits. That's bad.")
            return

        # Monthly habits
        self.cur.execute (
            f"SELECT habit_name, periodicity FROM habits WHERE owner = '{self.username}' AND periodicity = 'monthly';")
        monthly_habits = self.cur.fetchall()
        monthly_streaks = [(hab[0], self.compute_longest_streak_habit (hab[0], 'monthly')) for hab in monthly_habits]
        if monthly_streaks:
            max_monthly_streak = max(monthly_streaks, key=lambda e:e[1])
            print (
                f" The longest monthly streak of {max_monthly_streak[1]} month(s) you got for habit '{max_monthly_streak[0]}'.")
        else:
            print ("No monthly Streaks.")
            return

    # also for user guidance to choose a habit and see the longest streak
    def longest_streak_habit(self):
        """
        Shows the longest streak for a chosen habit.

        Asks the user for which habit they want to see the longest streak.
        Automatically filters if the habit is daily, weekly, or monthly.
        Uses the functions get_habit(), compute_longest_daily_streak_habit(), compute_longest_weekly_streak_habit(),
        and compute_longest_monthly_streak_habit().
        """
        habit_name = questionary.select("Choose a habit to see the longest streak:",choices = self.show_all()).ask()
        existing_habit = self.get_habit(habit_name)

        if existing_habit:
            periodicity = existing_habit.periodicity
            streak = self.compute_longest_streak_habit(habit_name, periodicity)
            streak_unit = "day(s)" if periodicity == "daily" else "week(s)" if periodicity == "weekly" else "month(s)"

            if streak is not None:
                print ( f"The longest streak of {habit_name} is: {streak} {streak_unit}" )
            else:
                print ( f"No streak data available for {habit_name}." )
        else:
            print ( "This habit does not exist." )
            return

        # function to define and calculate the streaks

    def compute_streak(self, habit_name, periodicity):
        """
        Computes the current streak of a habit based on its periodicity (daily, weekly, or monthly).
        The function analyzes the most recent dates of habit completion and calculates how many
        consecutive periods the habit has been maintained up to the current date.

        Parameters
        ----------
        habit_name : str
        The name of the habit for which the current streak is to be calculated.
        periodicity : str
        The periodicity of the habit. It can be 'daily', 'weekly', or 'monthly'.
        This parameter determines how the current streak is computed.

        Returns
        -------
        int
        The current streak count, which is the number of consecutive periods (as defined by
        the periodicity) that the habit has been maintained up to now.
        Returns 0 if there are no consecutive periods up to the current date or if no progress
        data is available.

        Notes
        -----
        - The function retrieves the habit's progress data and sorts it in reverse chronological order.
        - For 'daily' periodicity, it counts the streak by checking each date against the preceding day.
        - For 'weekly' periodicity, it compares the ISO week number and year of each date.
        - For 'monthly' periodicity, it compares the month and year of each date.
        - The streak is incremented for each consecutive period found and is broken when a period is missed.
        - The function returns the count of the current consecutive streak leading up to today's date.
        """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity=periodicity)
        if not habit_progress_total:
            return 0

        habits = [datetime.strptime (hab[0], '%Y-%m-%d %H:%M:%S') for hab in reversed (habit_progress_total)
                  if hab[0] is not None]

        current_date = datetime.now()
        streak = 0

        if periodicity == 'daily':
            for habit_date in habits:
                # For daily streaks, compare days
                if habit_date.date() == current_date.date():
                    streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break

        elif periodicity == 'weekly':
            for habit_date in habits:
                # For weekly streaks, compare calendar weeks and year
                if habit_date.isocalendar()[1] == current_date.isocalendar()[
                    1] and habit_date.year == current_date.year:
                    streak += 1
                    current_date -= timedelta(weeks=1)
                else:
                    break

        elif periodicity == 'monthly':
            for habit_date in habits:
                if habit_date.month == current_date.month and habit_date.year == current_date.year:
                    streak += 1
                    # Adjust to the first day of the previous month
                    first_day_of_month = current_date.replace(day=1)
                    previous_month_last_day = first_day_of_month - timedelta ( days=1 )
                    current_date = previous_month_last_day
                else:
                    break
        return streak

    # background function to define and calculate the longest streak
    def compute_longest_streak_habit(self, habit_name, periodicity):
        """
                Computes the longest streak of a habit based on its periodicity.
            This function examines the historical progress data of a specific habit
            to determine the maximum number of consecutive streaks (daily, weekly, or monthly).

            Parameters
            ----------
            habit_name : str
                The name of the habit for which the longest streak is to be calculated.
            periodicity : str
                The periodicity of the habit, which can be 'daily', 'weekly', or 'monthly'.
                This determines how the streaks are calculated.

            Returns
            -------
            int
                The longest streak of consecutive periods for the given habit.
                Returns 0 if no progress data is available or if the habit has never been maintained
                consecutively for more than one period.

            Notes
            -----
            - The function retrieves the habit's progress data and analyzes each date in the data set.
            - For 'daily' habits, it counts streaks by days, incrementing the streak when two consecutive days are found.
            - For 'weekly' habits, it compares week numbers of the year, considering a streak continued if consecutive weeks are found.
            - For 'monthly' habits, it calculates the difference in months between dates, with a one-month difference indicating a continuation of the streak.
            - If a period is missed according to the habit's periodicity, the current streak ends, and a new count begins.
            - The function then returns the maximum streak count found in the data set.
            """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity=periodicity)
        if habit_progress_total is None:
            return 0

        habits = [datetime.strptime(hab[0], '%Y-%m-%d %H:%M:%S') for hab in reversed(habit_progress_total)
                  if hab[0] is not None]

        # Streak count logic
        max_streak = 0
        current_streak = 1

        for i in range (len(habits) - 1):
            if periodicity == 'daily' and (habits[i]-habits[i + 1]).days == 1:
                current_streak += 1

            elif periodicity == 'weekly':
                week1, week2 = habits[i].isocalendar()[1], habits[i + 1].isocalendar()[1]
                if week1-week2 == 1 or (week1 == 1 and week2>50):
                    current_streak += 1
                else:
                    max_streak = max(max_streak, current_streak)
                    current_streak = 1

            elif periodicity == 'monthly':
                month_diff =(habits[i].year-habits[i + 1].year)*12+habits[i].month-habits[i + 1].month
                if month_diff == 1:
                    current_streak += 1
                else:
                    max_streak = max(max_streak, current_streak)
                    current_streak = 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1

        max_streak = max(max_streak, current_streak)
        return max_streak








