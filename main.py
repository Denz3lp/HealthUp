"""
This document handles the main menu and acts as user guidance.

It imports the library 'questionary' as the Command Line Interface (CLI) that guides the user through the program.
It also imports the initial.py doc which launches the core functionalities of the program.
"""
import questionary
import initial

# creating and launching the Database.
initial.start_database()

# program start with intro message.
intro_message = "\n-----------------------------\n" \
                "Welcome to Health UP!\n" \
                "The Habit Tracker for a healthy new Lifestyle.\n" \
                "-------------------------------\n"
print(intro_message)

# nest step of the menu, User must create an account or login.
first_question = questionary.select(
    "New here? ", choices=[
        "Register",
        "Login"
    ]).ask()

if first_question == "Login":
    user = initial.login()
    print("Welcome back!\n")

elif first_question == "Register":
    print("\n Great that you want to join us! Let's set up your profile.\n")
    initial.register_user()
    print("\n now you can login:\n")
    user = initial.login()

# new user can choose from a set of predefined habits
user.choose_predefined_habit()

# definition of the main menu, that navigates user through options.
def menu():
    """
    Main menu function of the Health Up application. It serves as the user interface for
    interacting with the application's features.

    The function offers a variety of choices for the user, such as editing the user profile,
    managing habits, viewing activity overviews, and seeing statistics. Upon selection,
    the appropriate functions or methods are called to perform the requested actions.
    It uses a loop to continuously present these options until the user chooses to log out.

    The function handles the creation, modification, deletion, and progress tracking of habits.
    It also provides options to view different types of habits based on their periodicity and
    to access different statistical views regarding the user's habit streaks.

    Returns:
        None. The function facilitates user navigation and interaction within the application.
    """
    what_question = questionary.select("What do you want to do? ",
                                         choices=[
                                                "Edit User Profile",
                                                "Create, or Edit a Habit",
                                                "Activity Overview",
                                                "See Stats",
                                                "Logout"
                                         ]).ask()
    if what_question == "Edit User Profile":
        print("Aye. Let's edit your profile.\n")
        initial.get_user(user)
        user.update_profile()
        print("\nWhat do you want to do now?\n")
        menu()

    elif what_question == "Create, or Edit a Habit":
        habit_question = questionary.select("Do you want to: ",
                                            choices=[
                                                "Create a new habit",
                                                "Delete a habit",
                                                "Edit a habit",
                                                "Mark as done"
                                            ]).ask()

        if habit_question == "Create a new habit":
            print("Let us create your Habit.\n")
            new_habit = user.create_habit()
            user.store_habit_in_db(new_habit)
            print("\nWhats next?\n")
            menu()

        elif habit_question == "Delete a habit":
            user.delete_habit()
            print("\nWhat do you want to do next?\n")
            menu()

        elif habit_question == "Edit a habit":
            print("So then lets Edit a habit")
            user.update_habit()
            print("\nDone! What now?\n")
            menu()

        else:
            print("Do you want to finish a Habit?")
            user.is_completed()
            print("\nWhat do you want to do now?\n")
            menu()

    elif what_question == "Activity Overview":
        activity_question = questionary.select("Do you want to see...: ",
                                                    choices=[
                                                        "all habits",
                                                        "all monthly habits",
                                                        "all weekly habits",
                                                        "all daily habits",
                                                        "Back"
                                                    ] ).ask ()

        if activity_question == "all habits":
            print("You currently have these habits saved: \n")
            user.show_all()
            print("\nWhat do you want to do now?\n")
            menu()

        elif activity_question == "all monthly habits":
            print ("Your monthly habits are: \n")
            user.show_monthly_habits()
            print("\nWhat do you want to do now?\n")
            menu()

        elif activity_question == "all weekly habits":
            print("Your weekly habits are: \n")
            user.show_weekly_habits()
            print("\nWhat do you want to do now?\n")
            menu()

        else:
            print("Your daily habits are: \n")
            user.show_daily_habits()
            print("\nWhat do you want to do now?\n")
            menu()

    if what_question == "See Stats":
        stats_question = questionary.select("here you can choose what you want to see: ",
                                            choices=[
                                                "Show streak per habit",
                                                "Show longest streak per habit",
                                                "Show streak overview",
                                                "Show longest streak overview",
                                                "Back"
                                            ]).ask()

        if stats_question == "Show streak overview":
            user.streak_overview()
            print ( "\nWhat shall we do now?\n" )
            menu ()
        elif stats_question == "Show streak per habit":
            user.streak_habit()
            print ( "\nWhat else do you want so see?\n" )
            menu ()
        elif stats_question == "Show longest streak per habit":
            user.longest_streak_habit()
            print ( "\nWhat's next?\n" )
            menu ()
        elif stats_question == "Show longest streak overview":
            user.longest_streak_overview()
            print ( "\nWant to see more?\n" )
            menu ()
        else:
            print("\nWhat do you want to do now?\n")
            menu()

    if what_question == "Logout":
        print(f"\nSee you soon, {user.firstname}!\n")

# execution of the main function, starts user guidance.
menu()
