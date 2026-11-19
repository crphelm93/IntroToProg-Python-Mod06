# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions, classes,
#       and the separation of concerns pattern with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Colin,11/14/2026,Reorganized code into FileProcessor and IO classes
# ------------------------------------------------------------------------------------------ #
import json

# -- Data -- #
# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = ''  # Holds the choice made by the user.
students: list = []  # A table of student data (a list of dictionary rows)


# -- Processing -- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog: (Who, When, What)
    Colin,11/14/2026,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads JSON data from a file into a list of dictionary rows

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param file_name: string with the name of the file to read from
        :param student_data: list of dictionary rows to be filled with file data
        :return: list of dictionary rows with the student data
        """
        file = None
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except json.JSONDecodeError as e:
            IO.output_error_messages("The file does not contain valid JSON data.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error when reading the file!", e)
        finally:
            if file is not None and file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes a list of dictionary rows to a JSON file,
        then displays the data that was written

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param file_name: string with the name of the file to write to
        :param student_data: list of dictionary rows to be written to the file
        :return: None
        """
        file = None
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=2)
            file.close()
            print("The following data was saved to file!")
            IO.output_student_courses(student_data=student_data)
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a problem with writing to the file.\n"
                                     "Please check that the file is not open by another program.", e)
        finally:
            if file is not None and file.closed == False:
                file.close()


# -- Presentation (Input/Output) -- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    Colin,11/14/2026,Created Class
    Colin,11/14/2026,Added menu output and input functions
    Colin,11/14/2026,Added functions to input and display student data
    Colin,11/14/2026,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error message to the user,
        plus the technical error message when an exception is passed

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param message: string with the custom message to display
        :param error: the Exception object, if any (optional)
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param menu: string with the menu text to display
        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e, to avoid the technical message
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays each student registration as comma-separated values

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param student_data: list of dictionary rows to display
        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'{student["FirstName"]},{student["LastName"]},{student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name, last name, and course name
        from the user and adds them as a new row in the table

        ChangeLog: (Who, When, What)
        Colin,11/14/2026,Created function

        :param student_data: list of dictionary rows to add the new row to
        :return: list of dictionary rows with the new registration added
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a problem with your entered data.", e)
        return student_data


# -- Main Body of Script -- #
# When the program starts, read the file data into a list of dictionary rows (table)
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":  # Register a student for a course
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":  # Show current data
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":  # Save data to a file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":  # Exit the program
        break  # out of the loop

print("Program Ended")