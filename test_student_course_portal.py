"""
Tests for Student Course Portal
"""

import unittest
from student_course_portal import Student, Course, StudentCoursePortal


class TestStudent(unittest.TestCase):
    """Test cases for Student class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.student = Student("S001", "Alice Johnson", "alice@example.com")
        self.course = Course("CS101", "Intro to CS", "Dr. Brown")
    
    def test_student_creation(self):
        """Test student creation"""
        self.assertEqual(self.student.student_id, "S001")
        self.assertEqual(self.student.name, "Alice Johnson")
        self.assertEqual(self.student.email, "alice@example.com")
        self.assertEqual(len(self.student.enrolled_courses), 0)
    
    def test_enroll_in_course(self):
        """Test enrolling in a course"""
        result = self.student.enroll_in_course(self.course)
        self.assertTrue(result)
        self.assertIn(self.course, self.student.enrolled_courses)
    
    def test_enroll_in_same_course_twice(self):
        """Test enrolling in the same course twice"""
        self.student.enroll_in_course(self.course)
        result = self.student.enroll_in_course(self.course)
        self.assertFalse(result)
        self.assertEqual(len(self.student.enrolled_courses), 1)
    
    def test_drop_course(self):
        """Test dropping a course"""
        self.student.enroll_in_course(self.course)
        result = self.student.drop_course(self.course)
        self.assertTrue(result)
        self.assertNotIn(self.course, self.student.enrolled_courses)
    
    def test_drop_course_not_enrolled(self):
        """Test dropping a course not enrolled in"""
        result = self.student.drop_course(self.course)
        self.assertFalse(result)


class TestCourse(unittest.TestCase):
    """Test cases for Course class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.course = Course("CS101", "Intro to CS", "Dr. Brown", max_capacity=2)
        self.student1 = Student("S001", "Alice", "alice@example.com")
        self.student2 = Student("S002", "Bob", "bob@example.com")
        self.student3 = Student("S003", "Carol", "carol@example.com")
    
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(self.course.course_id, "CS101")
        self.assertEqual(self.course.name, "Intro to CS")
        self.assertEqual(self.course.instructor, "Dr. Brown")
        self.assertEqual(self.course.max_capacity, 2)
        self.assertEqual(len(self.course.enrolled_students), 0)
    
    def test_add_student(self):
        """Test adding a student to a course"""
        result = self.course.add_student(self.student1)
        self.assertTrue(result)
        self.assertIn(self.student1, self.course.enrolled_students)
    
    def test_add_student_when_full(self):
        """Test adding a student when course is full"""
        self.course.add_student(self.student1)
        self.course.add_student(self.student2)
        result = self.course.add_student(self.student3)
        self.assertFalse(result)
        self.assertEqual(len(self.course.enrolled_students), 2)
    
    def test_remove_student(self):
        """Test removing a student from a course"""
        self.course.add_student(self.student1)
        result = self.course.remove_student(self.student1)
        self.assertTrue(result)
        self.assertNotIn(self.student1, self.course.enrolled_students)
    
    def test_is_full(self):
        """Test checking if course is full"""
        self.assertFalse(self.course.is_full())
        self.course.add_student(self.student1)
        self.assertFalse(self.course.is_full())
        self.course.add_student(self.student2)
        self.assertTrue(self.course.is_full())


class TestStudentCoursePortal(unittest.TestCase):
    """Test cases for StudentCoursePortal class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.portal = StudentCoursePortal()
    
    def test_add_student(self):
        """Test adding a student to the portal"""
        result = self.portal.add_student("S001", "Alice", "alice@example.com")
        self.assertTrue(result)
        self.assertIsNotNone(self.portal.get_student("S001"))
    
    def test_add_duplicate_student(self):
        """Test adding a duplicate student"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        result = self.portal.add_student("S001", "Bob", "bob@example.com")
        self.assertFalse(result)
    
    def test_add_course(self):
        """Test adding a course to the portal"""
        result = self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        self.assertTrue(result)
        self.assertIsNotNone(self.portal.get_course("CS101"))
    
    def test_add_duplicate_course(self):
        """Test adding a duplicate course"""
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        result = self.portal.add_course("CS101", "Data Structures", "Dr. Green")
        self.assertFalse(result)
    
    def test_enroll_student_in_course(self):
        """Test enrolling a student in a course"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        result = self.portal.enroll_student_in_course("S001", "CS101")
        self.assertTrue(result)
        
        student = self.portal.get_student("S001")
        course = self.portal.get_course("CS101")
        self.assertIn(course, student.enrolled_courses)
        self.assertIn(student, course.enrolled_students)
    
    def test_enroll_nonexistent_student(self):
        """Test enrolling a non-existent student"""
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        result = self.portal.enroll_student_in_course("S999", "CS101")
        self.assertFalse(result)
    
    def test_enroll_in_nonexistent_course(self):
        """Test enrolling in a non-existent course"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        result = self.portal.enroll_student_in_course("S001", "CS999")
        self.assertFalse(result)
    
    def test_enroll_in_full_course(self):
        """Test enrolling in a full course"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_student("S002", "Bob", "bob@example.com")
        self.portal.add_student("S003", "Carol", "carol@example.com")
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown", max_capacity=2)
        
        self.portal.enroll_student_in_course("S001", "CS101")
        self.portal.enroll_student_in_course("S002", "CS101")
        result = self.portal.enroll_student_in_course("S003", "CS101")
        self.assertFalse(result)
    
    def test_drop_student_from_course(self):
        """Test dropping a student from a course"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        self.portal.enroll_student_in_course("S001", "CS101")
        
        result = self.portal.drop_student_from_course("S001", "CS101")
        self.assertTrue(result)
        
        student = self.portal.get_student("S001")
        course = self.portal.get_course("CS101")
        self.assertNotIn(course, student.enrolled_courses)
        self.assertNotIn(student, course.enrolled_students)
    
    def test_list_students(self):
        """Test listing all students"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_student("S002", "Bob", "bob@example.com")
        students = self.portal.list_students()
        self.assertEqual(len(students), 2)
    
    def test_list_courses(self):
        """Test listing all courses"""
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        self.portal.add_course("CS201", "Data Structures", "Dr. Green")
        courses = self.portal.list_courses()
        self.assertEqual(len(courses), 2)
    
    def test_get_student_courses(self):
        """Test getting courses for a student"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        self.portal.add_course("CS201", "Data Structures", "Dr. Green")
        self.portal.enroll_student_in_course("S001", "CS101")
        self.portal.enroll_student_in_course("S001", "CS201")
        
        courses = self.portal.get_student_courses("S001")
        self.assertEqual(len(courses), 2)
    
    def test_get_course_students(self):
        """Test getting students in a course"""
        self.portal.add_student("S001", "Alice", "alice@example.com")
        self.portal.add_student("S002", "Bob", "bob@example.com")
        self.portal.add_course("CS101", "Intro to CS", "Dr. Brown")
        self.portal.enroll_student_in_course("S001", "CS101")
        self.portal.enroll_student_in_course("S002", "CS101")
        
        students = self.portal.get_course_students("CS101")
        self.assertEqual(len(students), 2)


if __name__ == "__main__":
    unittest.main()
