C-- Create the database
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- Create students table first
CREATE TABLE students (
    student_id INT NOT NULL AUTO_INCREMENT,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    department VARCHAR(50),
    PRIMARY KEY (student_id)
);

-- Then create results table referencing student_id
CREATE TABLE results (
    result_id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    subject VARCHAR(100),
    marks INT,
    PRIMARY KEY (result_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

