import os
MAX_USERS = 100
MAX_NOTES = 100
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 50
MAX_NOTE_LENGTH = 200
class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.notes = []
        self.noteCount = 0

def Encrypt(input_str):
    encrypted_str = ""
    for char in input_str:
        te= chr(ord(char) ^ 5)
        encrypted_str += te
    return encrypted_str

def Decrypt(input_str):
    return Encrypt(input_str)  
def Load(users):
    userCount = 0
    try:
        with open("user_data.txt", "r") as file:
            while userCount < MAX_USERS:
                line = file.readline()
                if not line:
                    break
                username, password = line.strip().split()
                username = Decrypt(username)
                password = Decrypt(password)
                new_user = User()
                new_user.username = username
                new_user.password = password

                while True:
                    note = file.readline().strip()
                    if not note:
                        break
                    new_user.notes.append(Decrypt(note))
                    new_user.noteCount += 1

                users.append(new_user)
                userCount += 1
    except FileNotFoundError:
        print("Error: Unable to open user data file.")
        return False
    return True

def Upload(users):
    try:
        with open("user_data.txt", "w") as file:
            for user in users:
                encrypted_username = Encrypt(user.username)
                encrypted_password = Encrypt(user.password)
                file.write(f"{encrypted_username} {encrypted_password}\n")
                for note in user.notes:
                    encrypted_note = Encrypt(note)
                    file.write(f"{encrypted_note}\n")
                file.write("\n")
    except IOError:
        print("Error: Unable to open user data file for saving.")
        return False
    return True

def FindUser(username, users):
    for user in users:
        if user.username == username:
            return user
    return None

def SignUp(users):
    if len(users) >= MAX_USERS:
        print("Error: Maximum number of users reached.")
        return

    new_user = User()
    new_user.username = input("Enter a username: ")

    if FindUser(new_user.username, users):
        print("Username already exists. Please choose a different one.")
        return

    new_user.password = input("Enter a password: ")
   
    users.append(new_user)
    print("Registration successful!")

def Login(users):
    username = input("Enter your username: ")

    cur_obj = FindUser(username, users)
    if cur_obj is None:
        print("Login failed. User does not exist.")
        return None

    password = input("Enter your password: ")

    if cur_obj.password == password:
        print("Login successful!")
        return cur_obj
    else:
        print("Login failed. Invalid password.")
        return None

def AddNote(cur_obj):
    if cur_obj is None:
        print("You must be logged in to add a note.")
        return

    if cur_obj.noteCount < MAX_NOTES:
        note = input("Enter your note: ")
        cur_obj.notes.append(note)
        cur_obj.noteCount += 1
        print("Note added!")
    else:
        print("Maximum number of notes reached.")

def DelNote(cur_obj):
    if cur_obj is None:
        print("You must be logged in to add a note.")
        return

    cur_obj.notes.clear()
    cur_obj.noteCount -= 1
    print("Note deleted!")

def ViewNotes(cur_obj):
    if cur_obj is None:
        print("You must be logged in to view notes.")
        return

    print("Your Notes:")
    for note in cur_obj.notes:
        print(note)

def main():
    users = []
    Load(users)

    cur_obj = None
    while True:
        print("Menu:")
        print("1. Sign up")
        print("2. Login")
        print("3. Add Note")
        print("4. Show Notes")
        print("5. Delete Notes")
        print("6. Save and Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            SignUp(users)
        elif choice == 2:
            if cur_obj is None:
                cur_obj = Login(users)
                if cur_obj is not None:
                    print(f"Welcome, {cur_obj.username}!")
            else:
                print("You are already logged in as {cur_obj.username}. If you want logout press 1")
                temp=int(input("Else press 0"))
                if(temp==1):
                     cur_obj = Login(users)
                     if cur_obj is not None:
                         print(f"Welcome, {cur_obj.username}!")
                    
        elif choice == 3:
            AddNote(cur_obj)
        elif choice == 4:
            ViewNotes(cur_obj)
        elif choice == 5:
            DelNote(cur_obj)
        elif choice == 6:
            if Upload(users):
                print("Exiting program.")
            else:
                print("Failed to save user data.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

