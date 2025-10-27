def get_letter_grade(points):
    if points >= 90:
        return 'A'
    elif points >= 80:
        return 'B'
    elif points >= 70:
        return 'C'
    elif points >= 60:
        return 'D'
    else:
        return 'F'

my_courses = ["English", "Math", "CS"]

while True:
    for course in my_courses:
        while True:
            try:
                points = float(input(f"Enter point count for {course}: "))
                if 0 <= points <= 100:
                    break
                else:
                    print("Please enter a number between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        grade = get_letter_grade(points)
        print(f"Grade for {course}: {grade}")

    redo = input("Do you want to redo the grades? (yes/no): ").strip().lower()
    if redo != 'yes':
        print("Program ended.")
        break
