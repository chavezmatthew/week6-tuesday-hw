CREATE DATABASE workout;

USE workout;

CREATE TABLE members (
id INT AUTO_INCREMENT PRIMARY KEY,
member_name VARCHAR(75) NOT NULL,
email VARCHAR(150) NULL,
phone VARCHAR(16) NULL
);

CREATE TABLE workouts (
id INT AUTO_INCREMENT PRIMARY KEY,
workout_date DATE NOT NULL,
member_id INT,
FOREIGN KEY (member_id) REFERENCES members(id)
);

SELECT * FROM members;

ALTER TABLE workouts
MODIFY COLUMN workout_date VARCHAR(250) NOT NULL;

SELECT * FROM workouts;