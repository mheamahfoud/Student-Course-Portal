"""
Student Course Portal - A simple system for managing students and courses
"""


class Student:
    """Represents a student in the portal"""
    
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.enrolled_courses = []
    
    def enroll_in_course(self, course):
        """Enroll student in a course"""
        if course not in self.enrolled_courses:
            if course.add_student(self):
                self.enrolled_courses.append(course)
                return True
            return False
        return False
    
    def drop_course(self, course):
        """Drop a course"""
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            course.remove_student(self)
            return True
        return False
    
    def get_courses(self):
        """Get list of enrolled courses"""
        return self.enrolled_courses
    
    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Email: {self.email})"


class Course:
    """Represents a course in the portal"""
    
    def __init__(self, course_id, name, instructor, max_capacity=30):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.enrolled_students = []
    
    def add_student(self, student):
        """Add a student to the course"""
        if len(self.enrolled_students) >= self.max_capacity or student in self.enrolled_students:
            return False
        self.enrolled_students.append(student)
        return True
    
    def remove_student(self, student):
        """Remove a student from the course"""
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            return True
        return False
    
    def get_students(self):
        """Get list of enrolled students"""
        return self.enrolled_students
    
    def is_full(self):
        """Check if course is at capacity"""
        return len(self.enrolled_students) >= self.max_capacity
    
    def __str__(self):
        return f"Course(ID: {self.course_id}, Name: {self.name}, Instructor: {self.instructor}, Enrolled: {len(self.enrolled_students)}/{self.max_capacity})"


class StudentCoursePortal:
    """Main portal for managing students and courses"""
    
    def __init__(self):
        self.students = {}
        self.courses = {}
    
    def add_student(self, student_id, name, email):
        """Add a new student to the portal"""
        if student_id in self.students:
            return False
        student = Student(student_id, name, email)
        self.students[student_id] = student
        return True
    
    def add_course(self, course_id, name, instructor, max_capacity=30):
        """Add a new course to the portal"""
        if course_id in self.courses:
            return False
        course = Course(course_id, name, instructor, max_capacity)
        self.courses[course_id] = course
        return True
    
    def get_student(self, student_id):
        """Get a student by ID"""
        return self.students.get(student_id)
    
    def get_course(self, course_id):
        """Get a course by ID"""
        return self.courses.get(course_id)
    
    def enroll_student_in_course(self, student_id, course_id):
        """Enroll a student in a course"""
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        
        if student is None or course is None:
            return False
        
        if course.is_full():
            return False
        
        return student.enroll_in_course(course)
    
    def drop_student_from_course(self, student_id, course_id):
        """Drop a student from a course"""
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        
        if student is None or course is None:
            return False
        
        return student.drop_course(course)
    
    def list_students(self):
        """List all students"""
        return list(self.students.values())
    
    def list_courses(self):
        """List all courses"""
        return list(self.courses.values())
    
    def get_student_courses(self, student_id):
        """Get courses for a student"""
        student = self.get_student(student_id)
        if student:
            return student.get_courses()
        return []
    
    def get_course_students(self, course_id):
        """Get students enrolled in a course"""
        course = self.get_course(course_id)
        if course:
            return course.get_students()
        return []


def main():
    """Main function to demonstrate the portal"""
    portal = StudentCoursePortal()
    
    # Add some students
    portal.add_student("S001", "Alice Johnson", "alice@example.com")
    portal.add_student("S002", "Bob Smith", "bob@example.com")
    portal.add_student("S003", "Carol Davis", "carol@example.com")
    
    # Add some courses
    portal.add_course("CS101", "Introduction to Computer Science", "Dr. Brown", 2)
    portal.add_course("CS201", "Data Structures", "Dr. Green", 30)
    portal.add_course("MATH101", "Calculus I", "Dr. White", 30)
    
    # Display students and courses
    print("=" * 60)
    print("STUDENT COURSE PORTAL")
    print("=" * 60)
    
    print("\nStudents:")
    for student in portal.list_students():
        print(f"  {student}")
    
    print("\nCourses:")
    for course in portal.list_courses():
        print(f"  {course}")
    
    # Enroll students in courses
    print("\n" + "=" * 60)
    print("ENROLLING STUDENTS IN COURSES")
    print("=" * 60)
    
    enrollments = [
        ("S001", "CS101"),
        ("S001", "MATH101"),
        ("S002", "CS101"),
        ("S002", "CS201"),
        ("S003", "CS101"),  # This should fail - course is full
        ("S003", "CS201"),
    ]
    
    for student_id, course_id in enrollments:
        student = portal.get_student(student_id)
        course = portal.get_course(course_id)
        success = portal.enroll_student_in_course(student_id, course_id)
        status = "SUCCESS" if success else "FAILED"
        print(f"  {status}: Enrolling {student.name} in {course.name}")
    
    # Display enrollment results
    print("\n" + "=" * 60)
    print("ENROLLMENT RESULTS")
    print("=" * 60)
    
    print("\nCourses:")
    for course in portal.list_courses():
        print(f"  {course}")
        students = portal.get_course_students(course.course_id)
        if students:
            for student in students:
                print(f"    - {student.name}")
        else:
            print("    (No students enrolled)")
    
    print("\nStudents:")
    for student in portal.list_students():
        print(f"  {student}")
        courses = portal.get_student_courses(student.student_id)
        if courses:
            for course in courses:
                print(f"    - {course.name}")
        else:
            print("    (Not enrolled in any courses)")
    
    # Test dropping a course
    print("\n" + "=" * 60)
    print("DROPPING A COURSE")
    print("=" * 60)
    
    student = portal.get_student("S001")
    course = portal.get_course("MATH101")
    success = portal.drop_student_from_course("S001", "MATH101")
    status = "SUCCESS" if success else "FAILED"
    print(f"  {status}: Dropping {student.name} from {course.name}")
    
    print(f"\n  {student.name}'s courses after drop:")
    for course in portal.get_student_courses("S001"):
        print(f"    - {course.name}")


if __name__ == "__main__":
    main()
