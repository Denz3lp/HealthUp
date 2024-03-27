from unittest import TestCase
from freezegun import freeze_time
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import habit
import User
import initial

class Test(TestCase):
    def test_get_user(self):
        test_user = initial.get_user("Barbie")
        non_existing_user = initial.get_user("non_existing_user")
        print( 'the user:', test_user.username, 'exists')
        assert type(test_user) == User.UserClass
        assert non_existing_user is None

class TestUserClass(TestCase):
    def test_get_habit(self):
        user = initial.get_user("Barbie")
        existing_habit = User.UserClass.get_habit(user, "Sleep")
        non_existing_habit = User.UserClass.get_habit(user, "non_existing_habit")
        print('habit sleep exists')
        assert type(existing_habit) == habit.HabitClass
        assert non_existing_habit is None

    def test_show_all(self):
        user = initial.get_user("Barbie")
        print('all consisting habits')
        all_habits = ["Sleep", "Water", "Swimming", "Running", "Gym"]
        user_habits = User.UserClass.show_all(user)
        assert all_habits == user_habits

    def test_show_daily_habits(self):
        user = initial.get_user("Barbie")
        print ('all daily habits')
        daily_habits = ["Sleep", "Water"]
        user_habits = User.UserClass.show_daily_habits(user)
        assert daily_habits == user_habits

    @freeze_time ( "2024-03-27" )
    def test_compute_streak(self):
        user = initial.get_user("Barbie")
        streak_water = User.UserClass.compute_streak(user, "Water", "daily")
        streak_sleep = User.UserClass.compute_streak (user, "Sleep", "daily")
        streak_running = User.UserClass.compute_streak (user, "Running", "weekly")
        streak_gym = User.UserClass.compute_streak (user, "Gym", "monthly")
        streak_swimming = User.UserClass.compute_streak(user, "Swimming", "monthly")
        print ("the current streaks are: for sleep:", streak_sleep, 'for running:', streak_running,)
        print ("For Gym:", streak_gym, 'Streak for swimming:', streak_swimming,)
        print ("finally, for water:", streak_water)

        assert streak_sleep == 87
        assert streak_running == 13
        assert streak_gym == 3
        assert streak_swimming == 3
        assert streak_water == 0

    @freeze_time ( "2024-03-27" )
    def test_compute_longest_streak_habit(self):
        user = initial.get_user( "Barbie")
        streak_sleep = User.UserClass.compute_longest_streak_habit(user, "Sleep", "daily")
        streak_running = User.UserClass.compute_longest_streak_habit(user, "Running", "weekly")
        streak_gym = User.UserClass.compute_longest_streak_habit(user, "Gym", "monthly")
        streak_swimming = User.UserClass.compute_longest_streak_habit(user, "Swimming", "monthly")
        streak_water = User.UserClass.compute_longest_streak_habit(user, "Water", "daily")
        print("the longest streaks are: Streak for sleep in days:", streak_sleep, 'Streak (in weeks) for running:', streak_running,)
        print("the longest streaks (in months) are: Gym:", streak_gym, 'Streak for swimming:', streak_swimming,)
        print("the longest streak for water (in days) is:", streak_water)

        assert streak_sleep == 87
        assert streak_running == 13
        assert streak_gym == 3
        assert streak_swimming == 3
        assert streak_water == 86

# shortcut command to test in terminal: python -m unittest test_User.py