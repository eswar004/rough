import csv
import tkinter as tk
from tkinter import ttk

class StudentGradingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Grading App")

        self.filename = 'student_data.csv'
        self.student_data = self.read_data()

        self.create_widgets()

    def read_data(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                data = list(reader)
            return data
        except FileNotFoundError:
            return []

    def write_data(self):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = self.student_data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.student_data)

    def create_widgets(self):
        self.tree = ttk.Treeview(self.master, columns=('ID', 'Name', 'Grade'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Grade', text='Grade')

        for student in self.student_data:
            self.tree.insert('', 'end', values=(student['id'], student['name'], student['grade']))

        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        btn_display = tk.Button(btn_frame, text='Display Data', command=self.display_data)
        btn_display.grid(row=0, column=0, padx=5)

        btn_add = tk.Button(btn_frame, text='Add Student', command=self.add_student)
        btn_add.grid(row=0, column=1, padx=5)

        btn_update = tk.Button(btn_frame, text='Update Grade', command=self.update_grade)
        btn_update.grid(row=0, column=2, padx=5)

        btn_delete = tk.Button(btn_frame, text='Delete Student', command=self.delete_student)
        btn_delete.grid(row=0, column=3, padx=5)

        btn_average = tk.Button(btn_frame, text='Calculate Average', command=self.calculate_average)
        btn_average.grid(row=0, column=4, padx=5)

        btn_sort = tk.Button(btn_frame, text='Sort by Grade', command=self.sort_students_by_grade)
        btn_sort.grid(row=0, column=5, padx=5)

        btn_export = tk.Button(btn_frame, text='Export to Text File', command=self.export_to_text_file)
        btn_export.grid(row=0, column=6, padx=5)

        btn_exit = tk.Button(btn_frame, text='Exit', command=self.master.destroy)
        btn_exit.grid(row=0, column=7, padx=5)

    def display_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in self.student_data:
            self.tree.insert('', 'end', values=(student['id'], student['name'], student['grade']))

    def add_student(self):
        add_window = tk.Toplevel(self.master)
        add_window.title('Add Student')

        tk.Label(add_window, text='Name:').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(add_window, text='Grade:').grid(row=1, column=0, padx=10, pady=10)

        entry_name = tk.Entry(add_window)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        entry_grade = tk.Entry(add_window)
        entry_grade.grid(row=1, column=1, padx=10, pady=10)

        btn_add = tk.Button(add_window, text='Add', command=lambda: self.add_student_to_data(
            entry_name.get(), entry_grade.get(), add_window))
        btn_add.grid(row=2, column=0, columnspan=2, pady=10)

    def add_student_to_data(self, name, grade, add_window):
        new_id = len(self.student_data) + 1
        self.student_data.append({'id': new_id, 'name': name, 'grade': grade})
        self.write_data()
        add_window.destroy()
        self.display_data()

    def update_grade(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        student_id = self.tree.item(selected_item)['values'][0]

        update_window = tk.Toplevel(self.master)
        update_window.title('Update Grade')

        tk.Label(update_window, text=f'Updating grade for student ID: {student_id}').grid(row=0, column=0, columnspan=2,
                                                                                          padx=10, pady=10)
        tk.Label(update_window, text='New Grade:').grid(row=1, column=0, padx=10, pady=10)

        entry_grade = tk.Entry(update_window)
        entry_grade.grid(row=1, column=1, padx=10, pady=10)

        btn_update = tk.Button(update_window, text='Update', command=lambda: self.update_student_grade(
            student_id, entry_grade.get(), update_window))
        btn_update.grid(row=2, column=0, columnspan=2, pady=10)

    def update_student_grade(self, student_id, new_grade, update_window):
        for student in self.student_data:
            if int(student['id']) == student_id:
                student['grade'] = new_grade
                self.write_data()
                update_window.destroy()
                self.display_data()
                return
        update_window.destroy()

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        student_id = self.tree.item(selected_item)['values'][0]

        response = tk.messagebox.askyesno('Delete Student',
                                          f'Are you sure you want to delete student with ID {student_id}?')
        if response:
            for student in self.student_data:
                if int(student['id']) == student_id:
                    self.student_data.remove(student)
                    self.write_data()
                    self.display_data()
                    return

    def calculate_average(self):
        grades = [int(student['grade']) for student in self.student_data]
        if grades:
            average = sum(grades) / len(grades)
            tk.messagebox.showinfo('Average Grade', f'The average grade is: {average:.2f}')
        else:
            tk.messagebox.showinfo('Average Grade', 'No students in the dataset')

    def sort_students_by_grade(self):
        sorted_data = sorted(self.student_data, key=lambda x: int(x['grade']), reverse=True)
        self.display_sorted_data(sorted_data)

    def display_sorted_data(self, sorted_data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in sorted_data:
            self.tree.insert('', 'end', values=(student['id'], student['name'], student['grade']))

    def export_to_text_file(self):
        filename = 'students.txt'
        with open(filename, 'w') as file:
            for student in self.student_data:
                file.write(f"ID: {student['id']}, Name: {student['name']}, Grade: {student['grade']}\n")
        tk.messagebox.showinfo('Export to Text File', f'Data exported to {filename}')


def main():
    root = tk.Tk()
    app = StudentGradingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
