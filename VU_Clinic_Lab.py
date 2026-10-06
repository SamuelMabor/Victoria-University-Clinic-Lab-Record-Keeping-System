# Victoria University Clinic Lab Record Keeping System
# A simple program for beginners.
# The lab is FREE for Victoria University students, staff and other workers.
# Lab staff use it to add, view, search and save lab records.

FILE_NAME = "lab_records.txt"
STUDENTS_FILE = "registered_students.txt"   # one registration number per line

# List of tests offered by the lab
TESTS = {
    "1": "Malaria Test",
    "2": "Typhoid Test",
    "3": "Blood Group",
    "4": "Pregnancy Test",
    "5": "Urinalysis",
    "6": "Full Blood Count",
}

# Each record is a dictionary. All records are kept in this list.
records = []

# Registration numbers of students registered at Victoria University
registered_students = []


# ---------------------------------------------------------------
# CHECK THAT A STUDENT IS REGISTERED AT VICTORIA UNIVERSITY
# A registration number looks like this: VU-BCS-2507-2171-DAY
# ---------------------------------------------------------------
def reg_number_format_ok(reg_no):
    parts = reg_no.split("-")
    if len(parts) != 5:
        return False
    if parts[0] != "VU":
        return False
    if not parts[1].isalpha():              # course code e.g. BCS
        return False
    if not (parts[2].isdigit() and len(parts[2]) == 4):   # e.g. 2507
        return False
    if not (parts[3].isdigit() and len(parts[3]) == 4):   # e.g. 2171
        return False
    if not parts[4].isalpha():              # study session e.g. DAY
        return False
    return True


def load_registered_students():
    try:
        file = open(STUDENTS_FILE, "r")
        for line in file:
            line = line.strip().upper()
            if line != "":
                registered_students.append(line)
        file.close()
        print("Registered students list loaded:", len(registered_students))
    except FileNotFoundError:
        print("WARNING:", STUDENTS_FILE, "not found. Only the format of")
        print("the registration number will be checked.")


def student_is_registered(reg_no):
    if not reg_number_format_ok(reg_no):
        return False
    # If we have the list of registered students, the number must be in it
    if len(registered_students) > 0 and reg_no not in registered_students:
        return False
    return True


def id_exists(patient_id):
    for record in records:
        if record["id"] == patient_id:
            return True
    return False


# ---------------------------------------------------------------
# 1. ADD A RECORD (with input validation)
# ---------------------------------------------------------------
def add_record():
    print("\n--- Add New Lab Record ---")

    # Validation 1: patient ID must not be empty or already used
    while True:
        patient_id = input("Enter patient ID (e.g. P001): ").strip().upper()
        if patient_id == "":
            print("Error: ID cannot be empty.")
        elif id_exists(patient_id):
            print("Error: that ID is already used.")
        else:
            break

    # Validation 2: name must not be empty
    while True:
        name = input("Enter patient name: ").strip()
        if name == "":
            print("Error: name cannot be empty.")
        else:
            break

    # Validation 3: patient type must be 1, 2 or 3
    while True:
        print("Patient type: 1. Student  2. Staff  3. Other worker")
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            patient_type = "Student"
            break
        elif choice == "2":
            patient_type = "Staff"
            break
        elif choice == "3":
            patient_type = "Worker"
            break
        else:
            print("Error: please type 1, 2 or 3.")

    # DECISION RULE: a student must have a valid, registered reg number
    reg_no = "N/A"
    if patient_type == "Student":
        while True:
            reg_no = input("Enter registration number (or BACK to cancel): ").strip().upper()
            if reg_no == "BACK":
                print("Cancelled. Only registered students can use the lab.")
                return
            if student_is_registered(reg_no):
                print("Registration number accepted.")
                break
            else:
                print("Error: not a valid registered student number.")
                print("Example: VU-BCS-2507-2171-DAY")

    # Validation 4: test choice must be in the test list
    while True:
        print("Available tests:")
        for number in TESTS:
            print(" ", number + ".", TESTS[number])
        test_choice = input("Choose a test number: ").strip()
        if test_choice in TESTS:
            break
        else:
            print("Error: that test number does not exist.")

    test_name = TESTS[test_choice]

    # Validation 5: result must be Positive or Negative
    while True:
        result = input("Enter result (Positive/Negative): ").strip().capitalize()
        if result == "Positive" or result == "Negative":
            break
        else:
            print("Error: type Positive or Negative.")

    # Put everything in one record and save it in the list
    record = {
        "id": patient_id,
        "name": name,
        "type": patient_type,
        "regno": reg_no,
        "test": test_name,
        "result": result,
    }
    records.append(record)

    print("\nRecord added successfully! The test is free of charge.")

    # DECISION RULE: advise on positive results
    if result == "Positive":
        print("NOTE: Positive result - refer the patient to the clinic doctor.")


# ---------------------------------------------------------------
# 2. DISPLAY ALL RECORDS
# ---------------------------------------------------------------
def show_one(record):
    print("ID:", record["id"], "| Name:", record["name"],
          "| Type:", record["type"], "| Reg No:", record["regno"],
          "| Test:", record["test"], "| Result:", record["result"])


def display_records():
    print("\n--- All Lab Records ---")
    if len(records) == 0:
        print("No records found.")
    else:
        for record in records:
            show_one(record)


# ---------------------------------------------------------------
# 3. SEARCH FOR A RECORD (by patient ID, name or reg number)
# ---------------------------------------------------------------
def search_record():
    print("\n--- Search Record ---")
    word = input("Enter patient ID, name or reg number: ").strip().lower()
    found = False
    for record in records:
        if (word == record["id"].lower() or word in record["name"].lower()
                or word == record["regno"].lower()):
            show_one(record)
            found = True
    if not found:
        print("No record found for:", word)


# ---------------------------------------------------------------
# 4. CALCULATE VALUES (summary report)
# ---------------------------------------------------------------
def show_summary():
    print("\n--- Summary Report ---")
    total = len(records)
    if total == 0:
        print("No records yet.")
        return

    students = 0
    staff = 0
    workers = 0
    positive = 0
    test_count = {}          # counts how many times each test was done

    for record in records:
        if record["type"] == "Student":
            students = students + 1
        elif record["type"] == "Staff":
            staff = staff + 1
        else:
            workers = workers + 1

        if record["result"] == "Positive":
            positive = positive + 1

        name = record["test"]
        if name in test_count:
            test_count[name] = test_count[name] + 1
        else:
            test_count[name] = 1

    # Find the most requested test
    most_test = ""
    most_number = 0
    for name in test_count:
        if test_count[name] > most_number:
            most_number = test_count[name]
            most_test = name

    positive_rate = positive / total * 100

    print("Total tests done:", total)
    print("Students:", students, "| Staff:", staff, "| Other workers:", workers)
    print("Positive results:", positive)
    print("Positive rate:", round(positive_rate, 1), "%")
    print("Most requested test:", most_test, "(" + str(most_number) + ")")


# ---------------------------------------------------------------
# 6. SAVE RECORDS TO A TEXT FILE
# ---------------------------------------------------------------
def save_records():
    file = open(FILE_NAME, "w")
    for record in records:
        line = (record["id"] + "|" + record["name"] + "|" + record["type"] + "|"
                + record["regno"] + "|" + record["test"] + "|" + record["result"])
        file.write(line + "\n")
    file.close()
    print("Records saved to", FILE_NAME)


# ---------------------------------------------------------------
# 7. LOAD RECORDS FROM THE TEXT FILE
# ---------------------------------------------------------------
def load_records():
    try:
        file = open(FILE_NAME, "r")
        for line in file:
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            record = {
                "id": parts[0],
                "name": parts[1],
                "type": parts[2],
                "regno": parts[3],
                "test": parts[4],
                "result": parts[5],
            }
            records.append(record)
        file.close()
        print("Loaded", len(records), "record(s) from", FILE_NAME)
    except FileNotFoundError:
        print("No saved file yet. Starting with an empty list.")


# ---------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------
def main():
    print("=== Victoria University Clinic Lab Record Keeping System ===")
    load_registered_students()
    load_records()

    while True:
        print("\n1. Add a record")
        print("2. Display all records")
        print("3. Search for a record")
        print("4. Summary report")
        print("5. Save records")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            display_records()
        elif choice == "3":
            search_record()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            save_records()
        elif choice == "6":
            save_records()      # save automatically before leaving
            print("Goodbye!")
            break               # leave the loop = exit safely
        else:
            print("Invalid choice. Please type a number from 1 to 6.")


main()
