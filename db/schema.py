def create_tables(cursor):
    """Create all database tables if they don't exist"""
    # Kopierte bare det fra discord
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Users (
          userID INTEGER PRIMARY KEY AUTOINCREMENT,
          fName VARCHAR(32) NOT NULL,
          lName VARCHAR(32) NOT NULL,
          weight DECIMAL(4,1) CHECK (weight > 0),
          DOB DATE,
          sex CHAR(1),
          CHECK (sex IN ('M', 'F'))
        );
        CREATE TABLE IF NOT EXISTS Health (
          userID INT NOT NULL,
          date DATE NOT NULL,
          heartrate FLOAT,
          VO2max FLOAT,
          HRvariation INT,
          sleeptime FLOAT,
          PRIMARY KEY (userID, date),
          FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Goals (
          userID INT NOT NULL,
          goalName VARCHAR(32) NOT NULL,
          amount DECIMAL(8,2) NOT NULL,
          metric VARCHAR(8) NOT NULL,
          completed TINYINT NOT NULL,
          PRIMARY KEY (userID, goalName),
          FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Workout (
          workoutID INTEGER PRIMARY KEY AUTOINCREMENT,
          userID INT NOT NULL,
          startTime DATETIME NOT NULL,
          endTime DATETIME NOT NULL,
          maxHR INT,
          workoutType VARCHAR(20) NOT NULL,
          CHECK (endTime > startTime),
          CHECK (workoutType IN ('Run', 'Weightlift')),
          FOREIGN KEY(userID) REFERENCES Users(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Run (
          workoutID INT NOT NULL,
          intervalNr INT NOT NULL,
          distance DECIMAL(6,2) NOT NULL,
          pace CHAR(5) NOT NULL,
          incline DECIMAL(3,1),
          PRIMARY KEY (workoutID, intervalNr),
          FOREIGN KEY (workoutID) REFERENCES Workout(workoutID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS Exercise (
          exerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
          name VARCHAR(32) NOT NULL,
          muscleGroup VARCHAR(32)
        );
        CREATE TABLE IF NOT EXISTS Weightlift (
          workoutID INT NOT NULL,
          exerciseID INT NOT NULL,
          setNr INT NOT NULL CHECK (setNr > 0),
          reps INT NOT NULL CHECK (reps > 0),
          weight DECIMAL(4,1) CHECK (weight >= 0),
          PRIMARY KEY(workoutID, exerciseID, setNr),
          FOREIGN KEY(workoutID) REFERENCES Workout(workoutID) ON DELETE CASCADE,
          FOREIGN KEY(exerciseID) REFERENCES Exercise(exerciseID) ON DELETE CASCADE
        );

        -- Create views
        DROP VIEW IF EXISTS UserProgressOverview;
        CREATE VIEW UserProgressOverview AS
        SELECT 
            u.userID,
            u.fName,
            u.lName,
            COUNT(DISTINCT w.workoutID) AS total_workouts,
            SUM(strftime('%s', w.endTime) - strftime('%s', w.startTime)) / 60 AS total_workout_minutes,
            AVG(h.VO2max) AS avg_VO2max,
            AVG(h.HRvariation) AS avg_HRV,
            AVG(h.sleeptime) AS avg_sleep,
            COUNT(DISTINCT CASE WHEN g.completed = 1 THEN g.goalName END) AS completed_goals,
            COUNT(DISTINCT CASE WHEN g.completed = 0 THEN g.goalName END) AS pending_goals
        FROM 
            Users u
        LEFT JOIN 
            Workout w ON u.userID = w.userID
        LEFT JOIN 
            Health h ON u.userID = h.userID
        LEFT JOIN 
            Goals g ON u.userID = g.userID
        GROUP BY 
            u.userID, u.fName, u.lName;

        DROP VIEW IF EXISTS ExerciseEffectivenessAnalysis;
        CREATE VIEW ExerciseEffectivenessAnalysis AS
        SELECT 
            e.exerciseID,
            e.name AS exercise_name,
            e.muscleGroup,
            COUNT(DISTINCT w.workoutID) AS times_performed,
            COUNT(DISTINCT w.userID) AS users_performed,
            AVG(wl.weight) AS avg_weight,
            AVG(wl.reps) AS avg_reps,
            (
                SELECT COUNT(*)
                FROM Goals g
                WHERE g.userID = w.userID
                  AND g.completed = 1
                  AND g.goalName = 'Lift Weights'
            ) AS related_goals_completed
        FROM 
            Exercise e
        JOIN 
            Weightlift wl ON e.exerciseID = wl.exerciseID
        JOIN 
            Workout w ON wl.workoutID = w.workoutID
        GROUP BY 
            e.exerciseID, e.name, e.muscleGroup;
    ''')