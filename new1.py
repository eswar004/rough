import csv
import tkinter as tk
from tkinter import ttk
import os

# Function to read student data from CSV file
def read_student_data(student_number):
    if not os.path.exists('student_data.csv'):
        return None

    with open('student_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['StudentNumber'] == student_number:
                # Initialize semester keys if they don't exist
                for semester in ['Semester1', 'Semester2']:
                    row.setdefault(semester, {})
                return row
    return None

# Function to save student data to CSV file
def save_student_data(data):
    with open('student_data.csv', 'a', newline='') as file:
        fieldnames = ['StudentNumber', 'Name', 'Semester1', 'Semester2']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Function to handle login
def login():
    student_number = entry_student_number.get()
    student_data = read_student_data(student_number)

    if student_data:
        show_welcome_screen(student_data)
    else:
        label_status.config(text="Invalid student number")

# Function to show the welcome screen
def show_welcome_screen(student_data):
    login_frame.pack_forget()
    welcome_frame.pack()

    welcome_label.config(text=f"Welcome, {student_data['Name']}!")

# Function to add grades
def add_grades():
    semester = combo_semester.get()
    subject = entry_subject.get()
    grade = entry_grade.get()

    if semester and subject and grade:
        # Initialize semester keys if they don't exist
        student_data.setdefault(semester, {})

        student_data[semester][subject] = grade
        label_status_welcome.config(text="Grade added successfully")
        save_student_data(student_data)
    else:
        label_status_welcome.config(text="Please fill in all fields")

# Function to exit the application
def exit_app():
    root.destroy()


# Create main window
root = tk.Tk()
root.title("Student Grading System")

# Create login frame
login_frame = tk.Frame(root)
login_frame.pack(padx=20, pady=20)

label_student_number = tk.Label(login_frame, text="Student Number:")
label_student_number.grid(row=0, column=0, padx=10, pady=10)

entry_student_number = tk.Entry(login_frame)
entry_student_number.grid(row=0, column=1, padx=10, pady=10)

button_login = tk.Button(login_frame, text="Login", command=login)
button_login.grid(row=1, column=0, columnspan=2, pady=10)

label_status = tk.Label(login_frame, text="")
label_status.grid(row=2, column=0, columnspan=2)

# Create welcome frame
welcome_frame = tk.Frame(root)

welcome_label = tk.Label(welcome_frame, text="Welcome to Application")
welcome_label.pack(pady=20)

notebook = ttk.Notebook(welcome_frame)

# Add Grades Tab
grades_tab = ttk.Frame(notebook)
notebook.add(grades_tab, text='Add Grades')

label_semester = tk.Label(grades_tab, text="Semester:")
label_semester.grid(row=0, column=0, padx=10, pady=10)

combo_semester = ttk.Combobox(grades_tab, values=['Semester1', 'Semester2'])
combo_semester.grid(row=0, column=1, padx=10, pady=10)

label_subject = tk.Label(grades_tab, text="Subject:")
label_subject.grid(row=1, column=0, padx=10, pady=10)

entry_subject = tk.Entry(grades_tab)
entry_subject.grid(row=1, column=1, padx=10, pady=10)

label_grade = tk.Label(grades_tab, text="Grade:")
label_grade.grid(row=2, column=0, padx=10, pady=10)

entry_grade = tk.Entry(grades_tab)
entry_grade.grid(row=2, column=1, padx=10, pady=10)

button_add_grade = tk.Button(grades_tab, text="Add Grade", command=add_grades)
button_add_grade.grid(row=3, column=0, columnspan=2, pady=10)

label_status_welcome = tk.Label(grades_tab, text="")
label_status_welcome.grid(row=4, column=0, columnspan=2)

# Add Exit Tab
exit_tab = ttk.Frame(notebook)
notebook.add(exit_tab, text='Exit')

button_exit = tk.Button(exit_tab, text="Exit Application", command=exit_app)
button_exit.pack(pady=20)

notebook.pack()

# Initialize student_data dictionary
student_data = {}

root.mainloop()
