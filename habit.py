"""
This document contains the Habit Class.
It imports sqlite3.
"""
import sqlite3
from datetime import datetime, timedelta

# THE HABIT CLASS.
class HabitClass:
    """
    Habit Class
    Attributes
    ----------
    habit_name: str
        the name of the habit
    owner: str
        the owner aka the user who the habit belongs to
    periodicity: str
        the periodicity can either be 'monthly', 'weekly'  or 'daily'
    datetime_creation: datetime
        the date and time of when the habit is first created
    """

    # INIT METHOD.
    def __init__(self, habit_name, owner, periodicity, datetime_creation):
        """
        :param habit_name: str
            the name of the habit
        :param owner: str
            the owner aka the user who the habit belongs to
        :param periodicity: str
            the periodicity of the habit which can be 'weekly'  or 'daily'
        :param datetime_creation: datetime
            the date and time of when the habit was first created
        """
        self.habit_name = habit_name
        self.owner = owner
        self.periodicity = periodicity
        self.datetime_creation = datetime.now()

        from os.path import join, dirname, abspath
        db_path = join(dirname(abspath(__file__)), 'healthup.db')

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

