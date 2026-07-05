import DeCastro_books as books
import DeCastro_borrow as borrow
import DeCastro_logbook as logbook
import DeCastro_encryption as encryption
from cryptography.fernet import Fernet

# FUNCITON TO GENERATE A KEY 
def create_key():

    try:
        with open('key.key', 'rb'):
            pass

    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key','wb') as file_key:
            file_key.write(key)

def ensure_file_exists(file_name):
    
    # CHECK IF FILE EXISTS
    try:
        # OPEN THE FILE IN READ MODE
        with open(file_name, 'r'):
            pass
        
    except FileNotFoundError:
        # CREATE THE FILE IF IT DOES NOT EXIST
        with open(file_name, 'w') as file:
            file.write('') # CREATES AN EMPTY FILE
        encryption.encrypt_file(file_name) # ENCCRYPT NEWLY CREATED FILE

# FUNCITON TO CHECK IF FILE IS EMPTY OR NOT
def decrypt_on_startup(file_name):
    # SAFELY ATTEMPTS TO DECRYPT THE FILE AT STARTUP
    try:
        with open(file_name, 'r') as file:
            content = file.read().strip()
        
        # IF THE FILE HAS CONTENT (meaning it has an encrypted token), DECRYPT IT
        if content != "":
            encryption.decrypt_file(file_name)

    except Exception:
        # IF IT THROWS AN ERROR (like InvalidToken), THE FILE IS ALREADY PLAIN TEXT
        # THIS HANDLES CASES WHERE PROGRAM FORCEFULLY CLOSES IF ERRORS OCCUR
        pass


def main_interface():

    # GENERATE KEY FOR ENCRYPTION
    create_key()

    # FILE PATHS
    file_library = "library.txt"
    file_borrow_list = "borrow_list.txt"
    file_logbook = "logbook.txt"

    # ENSURE FILES EXISTS
    ensure_file_exists(file_library)
    ensure_file_exists(file_borrow_list)
    ensure_file_exists(file_logbook)

    # CHECK FILES CONTENT (EMPTY OR NOT)
    decrypt_on_startup(file_library)
    decrypt_on_startup(file_borrow_list)
    decrypt_on_startup(file_logbook)

    try:
        while True:
            print("\n    Library Inventory and Logging System")
            print("\t[1] Go to Library")
            print("\t[2] Borrow Books")
            print("\t[3] Logbook")
            print("\t[4] Exit")
            choice = input("\nEnter option number: ").strip()

            if choice == "1":
                # FILES ARE ALREADY DECRYPTED
                # PASS THEM TO MODULE
                books.books_module(file_library, file_borrow_list)
            
            elif choice == "2":
                # IF LIBRARY IS CURRENTLY EMPTY, USER CANNOT PROCEED TO BORROW BOOKS
                library = books.load_books_from_file(file_library)

                if not library:
                    print("\nCannot proceed to borrow books. There are currently no books in the library.")

                else:
                    borrow.borrow_module(file_library, file_borrow_list, file_logbook)

            elif choice == "3":
                logbook.logbook_module(file_logbook, file_library)

            elif choice == "4":
                print("\nThank you for using this system. Goodbye!")
                break # BREAKS THE LOOP AND GOES TO 'finally' CODE BLOCK
            else:
                print("\nInvalid user input. Please select a valid option.")
    finally:
        # IF THE APP CRASHES (Pressing Ctrl+C or ending the program abruptly),
        # OR PRESS [4] TO EXIT, THE FILES WILL BE SAFELY SAVED AND ENCRYPTED
        print("\n[SYSTEM] Securing and encrypting databases before exit...")
        encryption.encrypt_file("library.txt")
        encryption.encrypt_file("borrow_list.txt")
        encryption.encrypt_file("logbook.txt")

main_interface() # CALLS THE MAIN INTERFACE FUNCTION