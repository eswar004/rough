import csv


def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def write_data(filename, data):
    fieldnames = data[0].keys()
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def display_data(data):
    for row in data:
        print(f"ID: {row['id']}, Name: {row['name']}, Grade: {row['grade']}")


def add_student(data):
    name = input("Enter student name: ")
    grade = int(input("Enter student grade: "))
    new_id = len(data) + 1
    data.append({'id': new_id, 'name': name, 'grade': grade})
    print(f"New Student {name} added with ID {new_id}")


def update_grade(data):
    student_id = int(input("Enter student ID to update grade: "))
    for student in data:
        if int(student['id']) == student_id:
            new_grade = int(input("Enter new grade: "))
            student['grade'] = new_grade
            print(f"Grade updated for student {student['name']}")
            return
    print(f"Student with ID {student_id} not found")


def delete_student(data):
    student_id = int(input("Enter student ID to delete: "))
    for student in data:
        if int(student['id']) == student_id:
            data.remove(student)
            print(f"Student {student['name']} with ID {student_id} deleted")
            return
    print(f"Student with ID {student_id} not found")


def search_student_by_name(data):
    search_name = input("Enter student name to search: ")
    matching_students = [student for student in data if search_name.lower() in student['name'].lower()]
    if matching_students:
        print("Matching students:")
        display_data(matching_students)
    else:
        print(f"No students found with name '{search_name}'")


def calculate_average(data):
    grades = [int(student['grade']) for student in data]
    if grades:
        average = sum(grades) / len(grades)
        print(f"Average grade: {average:.2f}")
    else:
        print("No students in the dataset")


def sort_students_by_grade(data):
    sorted_data = sorted(data, key=lambda x: int(x['grade']), reverse=True)
    print("Students sorted by grade:")
    display_data(sorted_data)


def export_to_text_file(data):
    filename = 'students.txt'
    with open(filename, 'w') as file:
        for student in data:
            file.write(f"ID: {student['id']}, Name: {student['name']}, Grade: {student['grade']}\n")
    print(f"Data exported to {filename}")


def main():
    filename = 'student_data.csv'
    student_data = read_data(filename)

    while True:
        print("\n1. Display student data")
        print("2. Add a new student")
        print("3. Update student grade")
        print("4. Delete a student")
        print("5. Search for a student by name")
        print("6. Calculate average grade")
        print("7. Sort students by grade")
        print("8. Export data to text file")
        print("9. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9): ")

        if choice == '1':
            display_data(student_data)
        elif choice == '2':
            add_student(student_data)
        elif choice == '3':
            update_grade(student_data)
        elif choice == '4':
            delete_student(student_data)
        elif choice == '5':
            search_student_by_name(student_data)
        elif choice == '6':
            calculate_average(student_data)
        elif choice == '7':
            sort_students_by_grade(student_data)
        elif choice == '8':
            export_to_text_file(student_data)
        elif choice == '9':
            write_data(filename, student_data)
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, or 9.")


if __name__ == "__main__":
    main()
