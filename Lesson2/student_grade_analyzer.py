"""Student Grade Analyzer - Complete Solution

This program reads student records from grades.txt, analyzes valid grades,
provides a menu-driven interface for viewing data, and generates reports.
"""


def classify_grade(grade):
    """Return the classification and status of a grade."""
    if 90 <= grade <= 100:
        return ("Excellent", "Passed")
    elif 85 <= grade <= 89:
        return ("Very Good", "Passed")
    elif 80 <= grade <= 84:
        return ("Good", "Passed")
    elif 75 <= grade <= 79:
        return ("Satisfactory", "Passed")
    elif 0 <= grade < 75:
        return ("Needs Improvement", "Failed")
    else:
        return ("Invalid", "Invalid")  # Should not be reached with validation


def load_students(filename):
    """Read valid student records from a text file and return them as a list."""
    students = []
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Clean the line and skip blank lines
                line = line.strip()
                if not line:
                    continue
                
                # Split the record and check for exactly three fields
                parts = line.split(",")
                if len(parts) != 3:
                    continue  # Skip invalid records
                
                student_id = parts[0].strip()
                name = parts[1].strip()
                grade_str = parts[2].strip()
                
                # Convert and validate the grade
                try:
                    grade = float(grade_str)
                    if 0 <= grade <= 100:
                        # Append valid record as a dictionary
                        students.append({
                            "student_id": student_id,
                            "name": name,
                            "grade": grade
                        })
                except ValueError:
                    # Skip records with non-numeric grades
                    continue
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    
    return students


def calculate_statistics(students):
    """Calculate and return the class statistics."""
    if not students:
        return None
    
    total_grade = 0
    passed_count = 0
    failed_count = 0
    highest_student = students[0]
    lowest_student = students[0]
    
    # Use one loop to update all statistics
    for student in students:
        grade = student["grade"]
        total_grade += grade
        
        # Update pass/fail counts
        classification, status = classify_grade(grade)
        if status == "Passed":
            passed_count += 1
        else:
            failed_count += 1
        
        # Update highest and lowest
        if grade > highest_student["grade"]:
            highest_student = student
        if grade < lowest_student["grade"]:
            lowest_student = student
    
    # Calculate the average
    average = total_grade / len(students)
    
    # Return all results in a dictionary
    return {
        "num_students": len(students),
        "average": average,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "highest_student": highest_student,
        "lowest_student": lowest_student
    }


def display_students(students):
    """Display all student records in a formatted table."""
    if not students:
        print("No students to display.")
        return
    
    # Print column headings
    print("\nSTUDENT RECORDS")
    print("-" * 70)
    print(f"{'Student ID':<12} {'Name':<20} {'Grade':<8} {'Classification':<18} {'Status':<10}")
    print("-" * 70)
    
    # Loop through students and display each record
    for student in students:
        student_id = student["student_id"]
        name = student["name"]
        grade = student["grade"]
        classification, status = classify_grade(grade)
        
        # Shorten name if needed (display first 18 characters + "...")
        display_name = name[:18] + "..." if len(name) > 20 else name
        
        print(f"{student_id:<12} {display_name:<20} {grade:<8.2f} {classification:<18} {status:<10}")


def display_statistics(statistics):
    """Display the calculated class statistics."""
    if not statistics:
        print("No statistics available.")
        return
    
    print("\nCLASS STATISTICS")
    print("-" * 40)
    print(f"Number of students: {statistics['num_students']}")
    print(f"Class average: {statistics['average']:.2f}")
    print(f"Passed: {statistics['passed_count']}")
    print(f"Failed: {statistics['failed_count']}")
    
    highest = statistics['highest_student']
    lowest = statistics['lowest_student']
    print(f"Highest: {highest['name']} - {highest['grade']:.2f}")
    print(f"Lowest: {lowest['name']} - {lowest['grade']:.2f}")


def search_student(students, keyword):
    """Return records whose student number or name matches the keyword."""
    matches = []
    
    # Make keyword lowercase and remove extra whitespace
    keyword = keyword.lower().strip()
    
    if not keyword:
        return matches
    
    # Use a loop and partial, case-insensitive matching
    for student in students:
        student_id = student["student_id"].lower()
        name = student["name"].lower()
        
        if keyword in student_id or keyword in name:
            matches.append(student)
    
    return matches


def save_report(students, statistics, filename):
    """Write the student results and class statistics to a report file."""
    try:
        with open(filename, 'w') as file:
            # Write report title
            file.write("STUDENT GRADE REPORT\n")
            file.write("=" * 50 + "\n\n")
            
            # Write student records
            file.write("STUDENT RECORDS\n")
            file.write("-" * 70 + "\n")
            file.write(f"{'Student ID':<12} {'Name':<20} {'Grade':<8} {'Classification':<18} {'Status':<10}\n")
            file.write("-" * 70 + "\n")
            
            for student in students:
                student_id = student["student_id"]
                name = student["name"]
                grade = student["grade"]
                classification, status = classify_grade(grade)
                
                display_name = name[:18] + "..." if len(name) > 20 else name
                file.write(f"{student_id:<12} {display_name:<20} {grade:<8.2f} {classification:<18} {status:<10}\n")
            
            # Write statistics
            file.write("\n\nCLASS STATISTICS\n")
            file.write("-" * 40 + "\n")
            file.write(f"Number of students: {statistics['num_students']}\n")
            file.write(f"Class average: {statistics['average']:.2f}\n")
            file.write(f"Passed: {statistics['passed_count']}\n")
            file.write(f"Failed: {statistics['failed_count']}\n")
            
            highest = statistics['highest_student']
            lowest = statistics['lowest_student']
            file.write(f"Highest: {highest['name']} - {highest['grade']:.2f}\n")
            file.write(f"Lowest: {lowest['name']} - {lowest['grade']:.2f}\n")
            
            file.write("\n" + "=" * 50 + "\n")
            file.write("End of Report\n")
            
        print(f"Report successfully saved to '{filename}'.")
        
    except OSError as e:
        print(f"Error saving report: {e}")


def main():
    """Run the menu-driven Student Grade Analyzer."""
    print("Loading student records...")
    students = load_students("grades.txt")
    
    if not students:
        print("No valid student records were loaded.")
        return
    
    print(f"Loaded {len(students)} valid student records.")
    statistics = calculate_statistics(students)
    
    while True:
        print("\nSTUDENT GRADE ANALYZER")
        print("[1] Display all students")
        print("[2] Display class statistics")
        print("[3] Search for a student")
        print("[4] Save report")
        print("[5] Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            display_students(students)
        elif choice == "2":
            display_statistics(statistics)
        elif choice == "3":
            keyword = input("Enter student ID or name to search: ")
            matches = search_student(students, keyword)
            if matches:
                print(f"\nFound {len(matches)} matching student(s):")
                display_students(matches)
            else:
                print(f"No students found matching '{keyword}'.")
        elif choice == "4":
            save_report(students, statistics, "grade_report.txt")
        elif choice == "5":
            print("Thank you for using the Student Grade Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue


if __name__ == "__main__":
    main()