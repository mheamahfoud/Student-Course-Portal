# Student-Course-Portal

A simple Python-based system for managing students, courses, and course enrollments.

## Features

- **Student Management**: Add and manage student records with ID, name, and email
- **Course Management**: Create and manage courses with instructor and capacity limits
- **Enrollment System**: Enroll students in courses with capacity checks
- **Drop Courses**: Allow students to drop enrolled courses
- **Query System**: View students, courses, and enrollment information

## Installation

No external dependencies required. Just Python 3.6+.

```bash
git clone https://github.com/mheamahfoud/Student-Course-Portal.git
cd Student-Course-Portal
```

## Usage

### Running the Demo

Run the main program to see a demonstration of the portal:

```bash
python student_course_portal.py
```

### Using as a Library

```python
from student_course_portal import StudentCoursePortal

# Create a new portal
portal = StudentCoursePortal()

# Add students
portal.add_student("S001", "Alice Johnson", "alice@example.com")
portal.add_student("S002", "Bob Smith", "bob@example.com")

# Add courses
portal.add_course("CS101", "Introduction to Computer Science", "Dr. Brown", max_capacity=30)
portal.add_course("CS201", "Data Structures", "Dr. Green", max_capacity=25)

# Enroll students in courses
portal.enroll_student_in_course("S001", "CS101")
portal.enroll_student_in_course("S001", "CS201")

# List students and their courses
for student in portal.list_students():
    print(student)
    for course in portal.get_student_courses(student.student_id):
        print(f"  - {course.name}")

# Drop a course
portal.drop_student_from_course("S001", "CS201")
```

## Running Tests

Run the test suite using Python's built-in unittest:

```bash
python -m unittest test_student_course_portal -v
```

## Classes

### Student
Represents a student with:
- `student_id`: Unique identifier
- `name`: Student's full name
- `email`: Student's email address
- `enrolled_courses`: List of courses the student is enrolled in

### Course
Represents a course with:
- `course_id`: Unique identifier
- `name`: Course name
- `instructor`: Instructor's name
- `max_capacity`: Maximum number of students
- `enrolled_students`: List of enrolled students

### StudentCoursePortal
Main portal class that manages:
- Student registration
- Course creation
- Enrollment operations
- Querying students and courses

## Key Features

- **Capacity Management**: Prevents over-enrollment in courses
- **Duplicate Prevention**: Prevents duplicate student/course IDs and duplicate enrollments
- **Bidirectional Linking**: Maintains consistent relationships between students and courses
- **Simple API**: Easy-to-use methods for all operations

## License

MIT License