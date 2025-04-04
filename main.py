import os
import sys

class Student:
    def __init__(self, name="", class_="", entry_number=0, gpa=0.0, password=""):
        self.name = name
        self.class_ = class_
        self.entry_number = entry_number
        self.fees = 1000
        self.subjects = []  # List of (subject, grade) tuples
        self.gpa = gpa
        self.__password = password

    def add_subject(self, subject, grade):
        self.subjects.append((subject, grade))
        self.gpa = self.calculate_gpa()

    def remove_subject(self, subject):
        self.subjects = [(s, g) for s, g in self.subjects if s != subject]
        self.gpa = self.calculate_gpa()

    def calculate_gpa(self):
        if not self.subjects:
            return 0.0
        total = sum(grade for _, grade in self.subjects)
        return total / len(self.subjects)

    def view_subjects(self):
        print("Subjects: ")
        if not self.subjects:
            print("  No subjects enrolled")
            return

        for subject, grade in self.subjects:
            print(f"  {subject} - {grade:.2f}")

    def authenticate(self, password):
        return self.__password == password

    def display_info(self):
        print("\n========== STUDENT INFORMATION ==========")
        print(f"Name: {self.name}")
        print(f"Class: {self.class_}")
        print(f"Entry Number: {self.entry_number}")
        print(f"GPA: {self.gpa:.2f}")
        print(f"Fees: ${self.fees}")
        self.view_subjects()
        print("========================================\n")

    def update_password(self, old_pass, new_pass):
        if self.authenticate(old_pass):
            self.__password = new_pass
            return True
        return False


class Teacher:
    def __init__(self, name="", subject="", classes_to_teach=None, password=""):
        self.teacher_id = 0
        self.name = name
        self.subject = subject
        self.classes_to_teach = classes_to_teach if classes_to_teach else []
        self.__password = password

    def authenticate(self, password):
        return self.__password == password

    def view_teacher_details(self):
        print("\n========== TEACHER INFORMATION ==========")
        print(f"ID: {self.teacher_id}")
        print(f"Name: {self.name}")
        print(f"Subject: {self.subject}")
        print(f"Classes to Teach: ", end="")
        if not self.classes_to_teach:
            print("None")
        else:
            print(", ".join(self.classes_to_teach))
        print("========================================\n")

    def update_password(self, old_pass, new_pass):
        if self.authenticate(old_pass):
            self.__password = new_pass
            return True
        return False

    def add_class_to_teach(self, class_no):
        if class_no not in self.classes_to_teach:
            self.classes_to_teach.append(class_no)

    def remove_class_to_teach(self, class_no):
        if class_no in self.classes_to_teach:
            self.classes_to_teach.remove(class_no)


class Classroom:
    def __init__(self, class_no, incharge):
        self.class_no = class_no
        self.incharge = incharge
        self.students = {}  

    def add_student(self, student):
        self.students[student.entry_number] = student

    def remove_student(self, entry_number):
        if entry_number in self.students:
            del self.students[entry_number]

    def view_students(self):
        if not self.students:
            print("  No students in this class.")
            return

        sorted_students = sorted([(entry_number, student.name) for entry_number, student in self.students.items()])
        for entry_number, name in sorted_students:
            print(f"  Name: {name}, Entry Number: {entry_number}")

    def class_average(self):
        if not self.students:
            return 0.0
        total = sum(student.gpa for student in self.students.values())
        return total / len(self.students)

    def view_class_details(self):
        print("\n========== CLASS INFORMATION ==========")
        print(f"Class Number: {self.class_no}")
        print(f"Incharge: {self.incharge}")
        print(f"Number of students: {len(self.students)}")
        print("Students:")
        self.view_students()
        print(f"Class Average GPA: {self.class_average():.2f}")
        print("======================================\n")

    def get_student(self, entry_number):
        return self.students.get(entry_number)


class School:
    def __init__(self, school_name="Sitender's School of Science and Technology"):
        self.school_name = school_name
        self.classes = {}  # Dict with class_no as key and Classroom object as value
        self.teachers = {}  # Dict with teacher_id as key and Teacher object as value

    def add_class(self, classroom):
        self.classes[classroom.class_no] = classroom

    def remove_class(self, class_no):
        if class_no in self.classes:
            del self.classes[class_no]

    def add_teacher(self, teacher):
        self.teachers[teacher.teacher_id] = teacher

    def remove_teacher(self, teacher_id):
        if teacher_id in self.teachers:
            del self.teachers[teacher_id]

    def view_class_details(self, class_no):
        if class_no in self.classes:
            self.classes[class_no].view_class_details()
        else:
            print("Class not found.")

    def view_teacher_details(self, teacher_id):
        if teacher_id in self.teachers:
            self.teachers[teacher_id].view_teacher_details()
        else:
            print("Teacher not found.")

    def find_student(self, entry_number):
        for class_no, classroom in self.classes.items():
            student = classroom.get_student(entry_number)
            if student:
                return student
        return None

    def get_all_class_numbers(self):
        return list(self.classes.keys())

    def view_all_students(self):
        print("\n========== ALL STUDENTS ==========")
        found = False
        for class_no, classroom in self.classes.items():
            if classroom.students:
                found = True
                print(f"Class {class_no}:")
                classroom.view_students()
        if not found:
            print("No students enrolled in any class.")
        print("================================\n")

    def view_all_teachers(self):
        print("\n========== ALL TEACHERS ==========")
        if not self.teachers:
            print("No teachers in the system.")
        else:
            for teacher_id, teacher in self.teachers.items():
                print(f"ID: {teacher_id}, Name: {teacher.name}, Subject: {teacher.subject}")
        print("================================\n")


class Admin:
    def __init__(self, username, password, school):
        self.__username = username
        self.__password = password
        self.school = school

    def authenticate(self, username, password):
        return self.__username == username and self.__password == password

    def view_school_details(self):
        print("\n========== SCHOOL INFORMATION ==========")
        print(f"School Name: {self.school.school_name}")
        print(f"\nClasses ({len(self.school.classes)}):")
        for class_no, classroom in self.school.classes.items():
            print(f"  Class Number: {class_no}, Incharge: {classroom.incharge}")
        print(f"\nTeachers ({len(self.school.teachers)}):")
        for teacher_id, teacher in self.school.teachers.items():
            print(f"  Teacher ID: {teacher_id}, Name: {teacher.name}, Subject: {teacher.subject}")
        print("========================================\n")

    def add_teacher(self, teacher):
        self.school.add_teacher(teacher)

    def remove_teacher(self, teacher_id):
        self.school.remove_teacher(teacher_id)

    def add_class(self, classroom):
        self.school.add_class(classroom)

    def remove_class(self, class_no):
        self.school.remove_class(class_no)

    def view_fee_record(self):
        print("\n========== FEE RECORDS ==========")
        found = False
        for class_no, classroom in self.school.classes.items():
            if classroom.students:
                found = True
                print(f"Class {class_no}:")
                for entry_number, student in classroom.students.items():
                    print(f"  Student ID: {entry_number}, Name: {student.name}, Fees: ${student.fees}")
        if not found:
            print("No students enrolled in any class.")
        print("================================\n")

    def update_student_fee(self, entry_number, new_fee):
        for class_no, classroom in self.school.classes.items():
            student = classroom.get_student(entry_number)
            if student:
                student.fees = new_fee
                return True
        return False

    def update_teacher_password(self, teacher_id, old_pass, new_pass):
        if teacher_id in self.school.teachers:
            return self.school.teachers[teacher_id].update_password(old_pass, new_pass)
        return False

    def update_password(self, new_pass):
        self.__password = new_pass


class Interface:
    def __init__(self):
        self.school = School()
        self.admin = Admin("admin", "admin123", self.school)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_input_buffer(self):
        pass  # Python doesn't need this like C++

    def pause_screen(self):
        input("\nPress Enter to continue...")

    def main_menu(self):
        while True:
            self.clear_screen()
            print(f"===== {self.school.school_name} =====")
            print("1. Admin Login")
            print("2. Teacher Login")
            print("3. Student Login")
            print("4. Exit")
            choice = input("Enter your choice: ")

            try:
                choice = int(choice)
            except ValueError:
                continue

            if choice == 1:
                self.admin_login()
            elif choice == 2:
                self.teacher_login()
            elif choice == 3:
                self.student_login()
            elif choice == 4:
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause_screen()

    def admin_login(self):
        self.clear_screen()
        print("===== ADMIN LOGIN =====")
        username = input("Username: ")
        password = input("Password: ")

        if self.admin.authenticate(username, password):
            self.admin_menu()
        else:
            print("Invalid credentials.")
            self.pause_screen()

    def admin_menu(self):
        while True:
            self.clear_screen()
            print("===== ADMIN MENU =====")
            print("1. View School Details")
            print("2. Add Teacher")
            print("3. Remove Teacher")
            print("4. View All Teachers")
            print("5. Add Class")
            print("6. Remove Class")
            print("7. View Class Details")
            print("8. Add Student")
            print("9. View All Students")
            print("10. View Fee Records")
            print("11. Update Student Fee")
            print("12. Change Admin Password")
            print("13. Back to Main Menu")

            try:
                admin_choice = int(input("Enter your choice: "))
            except ValueError:
                continue

            if admin_choice == 1:
                self.admin.view_school_details()
                self.pause_screen()
            elif admin_choice == 2:
                self.add_teacher()
            elif admin_choice == 3:
                self.remove_teacher()
            elif admin_choice == 4:
                self.school.view_all_teachers()
                self.pause_screen()
            elif admin_choice == 5:
                self.add_class()
            elif admin_choice == 6:
                self.remove_class()
            elif admin_choice == 7:
                self.view_class_details()
            elif admin_choice == 8:
                self.add_student()
            elif admin_choice == 9:
                self.school.view_all_students()
                self.pause_screen()
            elif admin_choice == 10:
                self.admin.view_fee_record()
                self.pause_screen()
            elif admin_choice == 11:
                self.update_student_fee()
            elif admin_choice == 12:
                self.change_admin_password()
            elif admin_choice == 13:
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause_screen()

    def add_teacher(self):
        self.clear_screen()
        print("===== ADD TEACHER =====")

        name = input("Enter teacher name: ")
        subject = input("Enter subject: ")
        
        try:
            teacher_id = int(input("Enter teacher ID: "))
        except ValueError:
            print("Invalid ID. Teacher not added.")
            self.pause_screen()
            return

        if teacher_id in self.school.teachers:
            print("Teacher ID already exists.")
            self.pause_screen()
            return

        available_classes = self.school.get_all_class_numbers()
        if not available_classes:
            print("No classes available. Please add classes first.")
            self.pause_screen()
            return

        print("Available classes: " + ", ".join(available_classes))
        
        classes_input = input("Enter class numbers (separated by spaces): ")
        class_nos = classes_input.split()
        
        all_classes_exist = True
        classes_to_teach = []
        
        for class_no in class_nos:
            if class_no not in self.school.classes:
                print(f"Class {class_no} does not exist.")
                all_classes_exist = False
            else:
                classes_to_teach.append(class_no)

        if not all_classes_exist:
            print("Some classes don't exist. Teacher not added.")
            self.pause_screen()
            return

        password = input("Enter password: ")

        new_teacher = Teacher(name, subject, classes_to_teach, password)
        new_teacher.teacher_id = teacher_id
        self.admin.add_teacher(new_teacher)
        print("Teacher added successfully.")
        self.pause_screen()

    def remove_teacher(self):
        self.clear_screen()
        print("===== REMOVE TEACHER =====")

        if not self.school.teachers:
            print("No teachers in the system.")
            self.pause_screen()
            return

        self.school.view_all_teachers()

        try:
            teacher_id = int(input("Enter teacher ID to remove: "))
        except ValueError:
            print("Invalid ID.")
            self.pause_screen()
            return

        if teacher_id not in self.school.teachers:
            print("Teacher not found.")
        else:
            self.admin.remove_teacher(teacher_id)
            print("Teacher removed successfully.")
        self.pause_screen()

    def add_class(self):
        self.clear_screen()
        print("===== ADD CLASS =====")

        class_no = input("Enter class number: ")

        if class_no in self.school.classes:
            print("Class already exists.")
            self.pause_screen()
            return

        incharge = input("Enter class incharge: ")

        new_class = Classroom(class_no, incharge)
        self.admin.add_class(new_class)
        print("Class added successfully.")
        self.pause_screen()

    def remove_class(self):
        self.clear_screen()
        print("===== REMOVE CLASS =====")

        if not self.school.classes:
            print("No classes in the system.")
            self.pause_screen()
            return

        class_numbers = self.school.get_all_class_numbers()
        print("Available classes: " + ", ".join(class_numbers))

        class_no = input("Enter class number to remove: ")

        if class_no not in self.school.classes:
            print("Class does not exist.")
        else:
            self.admin.remove_class(class_no)
            print("Class removed successfully.")
        self.pause_screen()

    def view_class_details(self):
        self.clear_screen()
        print("===== VIEW CLASS DETAILS =====")

        if not self.school.classes:
            print("No classes in the system.")
            self.pause_screen()
            return

        class_numbers = self.school.get_all_class_numbers()
        print("Available classes: " + ", ".join(class_numbers))

        class_no = input("Enter class number: ")
        self.school.view_class_details(class_no)
        self.pause_screen()

    def add_student(self):
        self.clear_screen()
        print("===== ADD STUDENT =====")

        if not self.school.classes:
            print("No classes in the system. Please add a class first.")
            self.pause_screen()
            return

        class_numbers = self.school.get_all_class_numbers()
        print("Available classes: " + ", ".join(class_numbers))

        class_no = input("Enter class number: ")

        if class_no not in self.school.classes:
            print("Class does not exist.")
            self.pause_screen()
            return

        name = input("Enter student name: ")
        
        try:
            entry_number = int(input("Enter entry number: "))
        except ValueError:
            print("Invalid entry number.")
            self.pause_screen()
            return

        existing_student = self.school.find_student(entry_number)
        if existing_student:
            print("Entry number already exists.")
            self.pause_screen()
            return

        password = input("Enter password: ")

        gpa = 0.0
        new_student = Student(name, class_no, entry_number, gpa, password)

        try:
            num_subjects = int(input("Enter number of subjects: "))
        except ValueError:
            print("Invalid number.")
            self.pause_screen()
            return

        for i in range(num_subjects):
            subject = input(f"Enter subject name {i+1}: ")
            try:
                grade = float(input(f"Enter grade for {subject}: "))
                if grade < 0 or grade > 100:
                    print("Invalid grade. Using 0.0")
                    grade = 0.0
            except ValueError:
                print("Invalid grade. Using 0.0")
                grade = 0.0

            new_student.add_subject(subject, grade)

        self.school.classes[class_no].add_student(new_student)
        print("Student added successfully.")
        self.pause_screen()

    def update_student_fee(self):
        self.clear_screen()
        print("===== UPDATE STUDENT FEE =====")

        try:
            entry_number = int(input("Enter student entry number: "))
        except ValueError:
            print("Invalid entry number.")
            self.pause_screen()
            return

        student = self.school.find_student(entry_number)
        if not student:
            print("Student not found.")
            self.pause_screen()
            return

        print(f"Current fee: ${student.fees}")
        
        try:
            new_fee = int(input("Enter new fee amount: $"))
            if new_fee < 0:
                print("Invalid fee amount.")
                self.pause_screen()
                return
        except ValueError:
            print("Invalid fee amount.")
            self.pause_screen()
            return

        if self.admin.update_student_fee(entry_number, new_fee):
            print("Fee updated successfully.")
        else:
            print("Failed to update fee.")
        self.pause_screen()

    def change_admin_password(self):
        self.clear_screen()
        print("===== CHANGE ADMIN PASSWORD =====")

        current_pass = input("Enter current password: ")

        if not self.admin.authenticate("admin", current_pass):
            print("Incorrect current password.")
            self.pause_screen()
            return

        new_pass = input("Enter new password: ")
        confirm_pass = input("Confirm new password: ")

        if new_pass != confirm_pass:
            print("Passwords do not match.")
            self.pause_screen()
            return

        self.admin.update_password(new_pass)
        print("Password changed successfully.")
        self.pause_screen()

    def teacher_login(self):
        self.clear_screen()
        print("===== TEACHER LOGIN =====")

        try:
            teacher_id = int(input("Enter Teacher ID: "))
        except ValueError:
            print("Invalid ID.")
            self.pause_screen()
            return

        if teacher_id not in self.school.teachers:
            print("Teacher not found.")
            self.pause_screen()
            return

        password = input("Enter Password: ")

        if self.school.teachers[teacher_id].authenticate(password):
            self.teacher_menu(self.school.teachers[teacher_id])
        else:
            print("Invalid password.")
            self.pause_screen()

    def teacher_menu(self, teacher):
        while True:
            self.clear_screen()
            print("===== TEACHER MENU =====")
            print(f"Welcome, {teacher.name}!")
            print("1. View My Details")
            print("2. View My Classes")
            print("3. View Students in a Class")
            print("4. Update Grade for a Student")
            print("5. Change Password")
            print("6. Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                continue

            if choice == 1:
                teacher.view_teacher_details()
                self.pause_screen()
            elif choice == 2:
                self.view_teacher_classes(teacher)
            elif choice == 3:
                self.view_students_in_class(teacher)
            elif choice == 4:
                self.update_student_grade(teacher)
            elif choice == 5:
                self.change_teacher_password(teacher)
            elif choice == 6:
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause_screen()

    def view_teacher_classes(self, teacher):
        self.clear_screen()
        print("===== MY CLASSES =====")

        if not teacher.classes_to_teach:
            print("You are not assigned to any classes.")
        else:
            print("You teach the following classes:")
            for class_no in teacher.classes_to_teach:
                if class_no in self.school.classes:
                    cls = self.school.classes[class_no]
                    print(f"Class: {class_no}, Incharge: {cls.incharge}")
                    print(f"Number of students: {len(cls.students)}")
                    print(f"Class Average GPA: {cls.class_average():.2f}")
                    print()
        self.pause_screen()

    def view_students_in_class(self, teacher):
        self.clear_screen()
        print("===== VIEW STUDENTS IN CLASS =====")

        if not teacher.classes_to_teach:
            print("You are not assigned to any classes.")
            self.pause_screen()
            return

        print("Your classes: " + ", ".join(teacher.classes_to_teach))

        class_no = input("Enter class number: ")

        if class_no not in teacher.classes_to_teach:
            print("You don't teach this class.")
            self.pause_screen()
            return

        if class_no not in self.school.classes:
            print("Class not found.")
        else:
            print(f"Students in class {class_no}:")
            self.school.classes[class_no].view_students()
        self.pause_screen()

    def update_student_grade(self, teacher):
        self.clear_screen()
        print("===== UPDATE STUDENT GRADE =====")

        if not teacher.classes_to_teach:
            print("You are not assigned to any classes.")
            self.pause_screen()
            return

        print("Your classes: " + ", ".join(teacher.classes_to_teach))

        class_no = input("Enter class number: ")

        if class_no not in teacher.classes_to_teach:
            print("You don't teach this class.")
            self.pause_screen()
            return

        if class_no not in self.school.classes:
            print("Class not found.")
            self.pause_screen()
            return

        classroom = self.school.classes[class_no]
        
        if not classroom.students:
            print("No students in this class.")
            self.pause_screen()
            return

        print(f"Students in class {class_no}:")
        classroom.view_students()

        try:
            entry_number = int(input("Enter student entry number: "))
        except ValueError:
            print("Invalid entry number.")
            self.pause_screen()
            return

        student = classroom.get_student(entry_number)
        if not student:
            print("Student not found in this class.")
            self.pause_screen()
            return

        subject = teacher.subject
        
        has_subject = False
        for subj, _ in student.subjects:
            if subj == subject:
                has_subject = True
                break

        if not has_subject:
            print(f"This student is not enrolled in {subject}.")
            choice = input("Do you want to add this subject? (y/n): ")
            if choice.lower() != 'y':
                self.pause_screen()
                return

        try:
            grade = float(input(f"Enter new grade for {subject}: "))
            if grade < 0 or grade > 100:
                print("Invalid grade.")
                self.pause_screen()
                return
        except ValueError:
            print("Invalid grade.")
            self.pause_screen()
            return

        if has_subject:
            for i, (subj, _) in enumerate(student.subjects):
                if subj == subject:
                    student.subjects[i] = (subject, grade)
                    break
            student.gpa = student.calculate_gpa()
        else:
            student.add_subject(subject, grade)

        print("Grade updated successfully.")
        self.pause_screen()

    def change_teacher_password(self, teacher):
        self.clear_screen()
        print("===== CHANGE PASSWORD =====")

        old_pass = input("Enter current password: ")
        new_pass = input("Enter new password: ")
        confirm_pass = input("Confirm new password: ")

        if new_pass != confirm_pass:
            print("Passwords do not match.")
            self.pause_screen()
            return

        if teacher.update_password(old_pass, new_pass):
            print("Password changed successfully.")
        else:
            print("Current password is incorrect.")
        self.pause_screen()

    def student_login(self):
        self.clear_screen()
        print("===== STUDENT LOGIN =====")

        try:
            entry_number = int(input("Enter Entry Number: "))
        except ValueError:
            print("Invalid entry number.")
            self.pause_screen()
            return

        student = self.school.find_student(entry_number)
        if not student:
            print("Student not found.")
            self.pause_screen()
            return

        password = input("Enter Password: ")

        if student.authenticate(password):
            self.student_menu(student)
        else:
            print("Invalid password.")
            self.pause_screen()

    def student_menu(self, student):
        while True:
            self.clear_screen()
            print("===== STUDENT MENU =====")
            print(f"Welcome, {student.name}!")
            print("1. View My Information")
            print("2. View My Subjects and Grades")
            print("3. Check Fee Status")
            print("4. Change Password")
            print("5. Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                continue

            if choice == 1:
                student.display_info()
                self.pause_screen()
            elif choice == 2:
                self.view_student_grades(student)
            elif choice == 3:
                self.view_fee_status(student)
            elif choice == 4:
                self.change_student_password(student)
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause_screen()

    def view_student_grades(self, student):
        self.clear_screen()
        print("===== MY SUBJECTS AND GRADES =====")
        student.view_subjects()
        print(f"GPA: {student.gpa:.2f}")
        self.pause_screen()

    def view_fee_status(self, student):
        self.clear_screen()
        print("===== FEE STATUS =====")
        print(f"Name: {student.name}")
        print(f"Class: {student.class_}")
        print(f"Entry Number: {student.entry_number}")
        print(f"Fee Amount: ${student.fees}")
        self.pause_screen()

    def change_student_password(self, student):
        self.clear_screen()
        print("===== CHANGE PASSWORD =====")

        old_pass = input("Enter current password: ")
        new_pass = input("Enter new password: ")
        confirm_pass = input("Confirm new password: ")

        if new_pass != confirm_pass:
            print("Passwords do not match.")
            self.pause_screen()
            return

        if student.update_password(old_pass, new_pass):
            print("Password changed successfully.")
        else:
            print("Current password is incorrect.")
        self.pause_screen()


if __name__ == "__main__":
    interface = Interface()
    interface.main_menu()