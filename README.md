# Project: Health Up - a Habit Tracker for a healthy Life

## Table of Contents
1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Usage and Main Functionalities](#Usage-and-Main-Functionalities)
4. [Contributing](#Contributing)

## General Info
Health Up employs you to keep track of your chosen activities. This application was developed as part of an upskilling course (Data Analyst) of the IUAS. 

The app enables you to integrate positive, healthy habits into your life. 
You can create a user profile, select habits from a pre-installed list, and create your habits. You cannot only track your activities but also see what your current and longest streaks are. 

## Installation

**Requirements:** 
Make sure you have Python 3.10+ installed. You can download the latest version of Python [here](https://www.python.org/downloads/). 

**Req. Package:**
* [questionary](https://github.com/tmbo/questionary) (install via "pip install questionary")

**Req. Package to run the tests:** 
* [freezegun] (https://github.com/spulec/freezegun) (install via pip install freezegun)

**How To:**<be>
Download and extract the zip folder of this repository and the latest version of Python.
After successfully installing Python, open your Mac, Windows or Linux Terminal. First, install the required library packages (i.e questionary by typing "pip install questionary") into the command line of your console of choice. 
To start the program type: "Python filepath/foldername/main.py" into your command line (make sure you replace the placeholders with your file path). 
You should have successfully launched the application! 
Try it out and enjoy! 

You are free to use the database"healthup.db" or the test data to try out the main functionalities.
*For test usage please utilize the given healthup.db file or the available data in the "data" folder.*

To run the tests, download all files incl. the folder "test" onto your computer. Install freezegun with "pip install freezegun". Start the test by open the terminal, enter your filepath and call python -m unittest test_User.py. 

## Usage and Main Functionalities

#### 0. Register

* Creation of a user profile. 
* prompted to enter first and last name, username and password of choice. 
* If the username is already taken, the program asks to try another one. 
* If everything is completed correctly, the user profile is created. 
---
#### 1. Login
* Enter username and password. 
* New users haven't saved any habits yet, therefore a list of preset habits is prompted to choose from. 
* User can either choose to select or skip a habit with Y/N. 
---
#### 2. Edit User Profile
* User can change first and last name as well as the password. 
---
#### 3. Create, Change or Mark a Habit as completed
#####  3.1. Create a new habit 
* Creation of own habits: The user has to set a habit name and its periodicity (daily/weekly or monthly).
* The habit name cannot be changed after it has been created!
##### 3.2. Delete a habit
* To delete a habit, the user types in the name of the habit they wish to delete.        
##### 3.3. Change an existing habit
* To change the periodicity of an existing habit, the user has to enter the habit name.        
##### 3.4. Mark a habit as completed
* To track the habit progress, the user has to mark the habits as completed. 
* To mark the progress, the user types in the name of the habit. 
---
#### 4. Activity Overview
##### 4.1. All habits
* Shows a list of all saved habits. 
##### 4.2. All monthly habits
* Shows a list of all monthly habits.           
##### 4.3. All weekly habits
* Shows a list of all weekly habits.       
##### 4.4. All daily habits
* Shows a list of all daily habits. 
---
#### 5. See Stats
##### 5.1.  Streak overview
* Shows a list of all saved habits and their current streaks.  
##### 5.2. Streak per habit
* To see the current streak of a specific habit, the user is prompted to type in the name of the habit to check. 
##### 5.3. The longest streak per habit
* To check the longest streak for a specific habit, the user has to type in the name of the habit.     
##### 5.4. The longest streak overview 
* Displays the longest streaks for each periodicity. 

## Contributing 
This is my first development of a Python-based application utilizing OOP and functional Programming. Any comments, suggestions, or contributions are welcome. 

