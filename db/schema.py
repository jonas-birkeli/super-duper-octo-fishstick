import streamlit as st
from connection import get_connection


def create_tables():
    db = get_connection()

    # Users table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Users (
        userID INTEGER PRIMARY KEY AUTO_INCREMENT,
        fName VARCHAR(32) NOT NULL,
        lName VARCHAR(32) NOT NULL,
        weight FLOAT,
        DOB DATE,
        sex CHAR(1) CHECK (sex IN ('M', 'F'))
    )
    ''', commit=True)

    # Health table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Health (
        userID INTEGER,
        date DATE,
        heartrate FLOAT,
        VO2max FLOAT,
        HRvariation INTEGER,
        sleeptime FLOAT,
        sleepQuality INTEGER,
        PRIMARY KEY (userID, date),
        FOREIGN KEY (userID) REFERENCES Users(userID)
    )
    ''', commit=True)

    # Goals table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Goals (
        userID INTEGER,
        goalName VARCHAR(32),
        amount FLOAT NOT NULL,
        metric VARCHAR(8) NOT NULL,
        completed BOOLEAN DEFAULT 0,
        PRIMARY KEY (userID, goalName),
        FOREIGN KEY (userID) REFERENCES Users(userID)
    )
    ''', commit=True)

    # Workout table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Workout (
        workoutID INTEGER PRIMARY KEY AUTO_INCREMENT,
        userID INTEGER NOT NULL,
        starttime DATETIME NOT NULL,
        endtime DATETIME NOT NULL,
        maxHR INTEGER,
        workoutType VARCHAR(20) CHECK (workoutType IN ('Run', 'Weightlift')),
        FOREIGN KEY (userID) REFERENCES Users(userID)
    )
    ''', commit=True)

    # Run table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Run (
        workoutID INTEGER PRIMARY KEY,
        distance FLOAT,
        avgPace FLOAT,
        FOREIGN KEY (workoutID) REFERENCES Workout(workoutID)
    )
    ''', commit=True)

    # Intervals table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Intervals (
        workoutID INTEGER,
        intervalNr INTEGER,
        distance FLOAT,
        pace FLOAT,
        incline FLOAT,
        PRIMARY KEY (workoutID, intervalNr),
        FOREIGN KEY (workoutID) REFERENCES Run(workoutID)
    )
    ''', commit=True)

    # Weightlift table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Weightlift (
        workoutID INTEGER PRIMARY KEY,
        activeMinutes INTEGER,
        restMinutes INTEGER,
        FOREIGN KEY (workoutID) REFERENCES Workout(workoutID)
    )
    ''', commit=True)

    # ExerciseType table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS ExerciseType (
        exerciseID INTEGER PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(32) NOT NULL,
        musclegroup VARCHAR(32)
    )
    ''', commit=True)

    # Exercise table
    db.execute_query('''
    CREATE TABLE IF NOT EXISTS Exercise (
        workoutID INTEGER,
        exerciseID INTEGER,
        setNr INTEGER,
        reps INTEGER,
        weight FLOAT,
        PRIMARY KEY (workoutID, exerciseID, setNr),
        FOREIGN KEY (workoutID) REFERENCES Weightlift(workoutID),
        FOREIGN KEY (exerciseID) REFERENCES ExerciseType(exerciseID)
    )
    ''', commit=True)


def insert_sample_data():
    db = get_connection()

    # Check if we already have sample data
    db.execute_query("SELECT COUNT(*) FROM Users")
    if db.fetchone()[0] > 0:
        return

    exercise_types = [
        (1, "Bench Press", "Chest"),
        (2, "Squat", "Legs"),
        (3, "Deadlift", "Back"),
        (4, "Shoulder Press", "Shoulders"),
        (5, "Bicep Curl", "Arms")
    ]

    for ex_type in exercise_types:
        db.execute_query(
            "INSERT INTO ExerciseType (exerciseID, name, musclegroup) VALUES (?, ?, ?)",
            ex_type,
            commit=True
        )

    users = [
        (1, "Johan", "Bruh", 70.0, "2000-01-01", "M"),
        (2, "Jonas", "BruhBruh", 70.0, "2000-01-01", "M")
        (3, "Benny", "BruhBruhBruh", 70.0, "2000-01-01", "F")
        (4, "Torbjørn", "BruhBruhBruhBruh", 70.0, "2000-01-01", "M")
    ]

    for user in users:
        db.execute_query(
            "INSERT INTO Users (userID, fName, lName, weight, DOB, sex) VALUES (?, ?, ?, ?, ?, ?)",
            user,
            commit=True
        )

    goals = [
        (1, "Weight Loss", 10.0, "kg", 0),
        (1, "Run Distance", 5.0, "km", 1),
        (2, "Strength", 50.0, "kg", 0)
    ]

    for goal in goals:
        db.execute_query(
            "INSERT INTO Goals (userID, goalName, amount, metric, completed) VALUES (?, ?, ?, ?, ?)",
            goal,
            commit=True
        )


def initialize_database():
    create_tables()
    insert_sample_data()