DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    student_id INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
);
-- insert data into students table
INSERT INTO students (name, email) VALUES
('Robert', 'robert@gmail.com'),
('Collins', 'collins@gmail.com'),
('Sharon', 'sharon@gmail.com'),
('Nyairo', 'nyairo@gmail.com'),
('Fatuma', 'fatuma@gmail.com'),
('Kanye', 'kanye@gmail.com');

-- INSERT DATA INTO COURSES TABLE
INSERT INTO courses (course_name, student_id) VALUES
('Python', 1),
('JavaScript', 2),
('SQL', 3),
('React', 4),
('Flask', 1);


-- View all students

SELECT * FROM students;

-- View all courses

SELECT * FROM courses;

-- Find students who have courses

SELECT *
FROM students
WHERE id IN (
    SELECT student_id
    FROM courses
);

-- Find students who do not have courses

SELECT *
FROM students
WHERE id NOT IN (
    SELECT student_id
    FROM courses
);

-- Count the number of courses each student is enrolled in

SELECT
    name,
    email,
    (
        SELECT COUNT(*)
        FROM courses
        WHERE courses.student_id = students.id
    ) AS course_count
FROM students;
