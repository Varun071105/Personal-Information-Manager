import datetime
import json  # Import JSON for saving/loading data

# Helper function to load existing data
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to save data to file
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def task_manager():
    tasks = load_data("tasks.json")# Load tasks from file
    if not isinstance(tasks, list):
        tasks = []

    def add_task():
        new_task = input("Enter a task to add: ")
        tasks.append(new_task)
        save_data("tasks.json", tasks)  # Save updated tasks
        print(f"Task '{new_task}' added successfully!")

    def remove_task():
        remove_task = input("Enter the task to remove: ")
        if remove_task in tasks:
            tasks.remove(remove_task)
            save_data("tasks.json", tasks)  # Save updated tasks
            print(f"Task '{remove_task}' removed successfully!")
        else:
            print("Task not found!")

    def view_tasks():
        if tasks:
            print("\nCurrent Tasks:")
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
        else:
            print("No tasks available!")

    return {"add_task": add_task, "remove_task": remove_task, "view_tasks": view_tasks}


def notes():
    Note = load_data("notes.json")  # Load notes from file
    if not isinstance(Note, list):
        Note = []

    def add_note():
        new_notes = input("Enter notes: ")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Note.append({"note": new_notes, "timestamp": timestamp})
        save_data("notes.json", Note)  # Save updated notes
        print(f"Note added successfully at {timestamp}")
        
    def remove_note(): 
        if Note:
            print("\nSaved Notes:")
            for idx, entry in enumerate(Note, 1):
                print(f"{idx}. {entry['note']} (Added on {entry['timestamp']})")
            try:
                num = int(input("Enter the note number to remove: "))
                if 1 <= num <= len(Note):
                    removed_note = Note.pop(num - 1)
                    save_data("notes.json", Note)
                    print(f"Removed note: '{removed_note['note']}'")
                else:
                    print("Invalid note number!")
            except ValueError:
                print("Please enter a valid number!")
        else:
            print("No notes available to remove!")  
        

    def view_note():
        if Note:
            print("\nSaved Notes:")
            for idx, entry in enumerate(Note, 1):
                print(f"{idx}. {entry['note']} (Added on {entry['timestamp']})")
        else:
            print("No notes available!")

    return {"add_note": add_note, "remove_note": remove_note, "view_note": view_note}


def Contacts_book():
    book = load_data("contacts.json")  # Load contacts from file

    def add_number():
        Name = input("Enter NAME: ")
        Mobile_Number = input("Enter NUMBER: ")
        Relation = input("Enter Relation: ")
        book[Name] = {"PHONE NUMBER": Mobile_Number, "Relation": Relation}
        save_data("contacts.json", book)  # Save updated contacts
        print(f"Contact '{Name}' added successfully!")

    def remove_number():
        Name = input("Enter NAME to remove: ")
        if Name in book:
            del book[Name]
            save_data("contacts.json", book)  # Save updated contacts
            print(f"Contact '{Name}' removed successfully!")
        else:
            print("Contact not found.")

    def view_contacts():
        if book:
            print("\nContact List:")
            for name, details in book.items():
                print(f"{name}: {details}")
        else:
            print("No contacts available!")

    return {"add_number": add_number, "remove_number": remove_number, "view_contacts": view_contacts}


# ---------------------- MAIN MENU ----------------------
while True:
    print("\nPersonal Information Manager:")
    choice = input("Press 1,2,3 or 4 to exit:\n 1. Task Manager\n 2. Notes\n 3. ContactBook\n 4. Exit\n")
    if choice == "1":
        task_functions = task_manager()
        while True:
            action = input("\nChoose action:\n 1. Add Task\n 2. Remove Task\n 3. ViewTasks\n 4. Back to Main Menu\n")
            if action == "1":
                task_functions["add_task"]()
            elif action == "2":
                task_functions["remove_task"]()
            elif action == "3":
                task_functions["view_tasks"]()
            elif action == "4":
                break
            else:
                print("Invalid action!")
    elif choice == "2":
        note_functions = notes()
        while True:
            action = input("\nChoose action:\n 1. Add Note\n 2. Remove Note\n 3. ViewNotes\n 4. Back to Main Menu\n")
            if action == "1":
                note_functions["add_note"]()
            elif action == "2":
                note_functions["remove_note"]()
            elif action == "3":
                note_functions["view_note"]()
            elif action == "4":
                break
            else:
                print("Invalid action!")

    elif choice == "3":
        contact_functions = Contacts_book()
        while True:
             action = input("\nChoose action:\n 1. Add Contact\n 2. Remove Contact\n 3.View Contacts\n 4. Back to Main Menu\n")
             if action == "1":
                 contact_functions["add_number"]()
             elif action == "2":
                 contact_functions["remove_number"]()
             elif action == "3":
                 contact_functions["view_contacts"]()
             elif action == "4":
                 break
             else:
                 print("Invalid action!")

    elif choice == "4":
        print("Exiting Personal Information Manager. Goodbye!")
        break

    else:
        print("ERROR: Invalid Choice")
