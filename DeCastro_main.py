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

    return True

# FUNCITON TO CHECK IF FILE IS EMPTY OR NOT
def check_file_content(file_name):

    try:
        with open(file_name, 'r') as file:
            return file.read().strip != ""

    except FileNotFoundError:
        return False


def main_interface():

    # GENERATE KEY FOR ENCRYPTION
    create_key()

    # FILE PATHS
    file_library = "library.txt"
    file_borrow_list = "borrow_list.txt"
    file_logbook = "logbook.txt"

    # ENSURE FILES EXISTS
    library_exist = ensure_file_exists(file_library)
    borrow_list_exist = ensure_file_exists(file_borrow_list)
    logbook_exist = ensure_file_exists(file_logbook)

    # CHECK FILES CONTENT (EMPTY OR NOT)
    library_content = check_file_content(file_library)
    borrow_list_content = check_file_content(file_borrow_list)
    logbook_content = check_file_content(file_logbook)

    while True:
        print("\n    Library Inventory and Logging System")
        print("\t[1] Go to Library")
        print("\t[2] Borrow Books")
        print("\t[3] Logbook")
        print("\t[4] Exit")
        choice = input("\nEnter option number: ").strip()

        # DECRYPT FILE TO BE USED IN LIBRARY MODULES
        
        if choice == "1":
            try:
                if library_exist and library_content:
                    encryption.decrypt_file(file_library)

            except Exception as e:
                print(f"Error decrypting the file: {e}")

            books.books_module(file_library, file_borrow_list)
        
        elif choice == "2":
            # IF LIBRARY IS CURRENTLY EMPTY, USER CANNOT PROCEED TO BORROW BOOKS
            library = books.load_books_from_file(file_library)

            if not library:
                print("\nCannot proceed to borrow books. There are currently no books in the library.")

            else:
                try:
                    if borrow_list_exist and borrow_list_content:
                        encryption.decrypt_file(file_borrow_list)
                        
                except Exception as e:
                    print(f"Error decrypting the file: {e}")

                borrow.borrow_module(file_library, file_borrow_list, file_logbook)

        elif choice == "3":
            try:
                if logbook_exist and logbook_content:
                    encryption.decrypt_file(file_logbook)
            
            except Exception as e:
                print(f"Error decrypting the file: {e}")

            logbook.logbook_module(file_logbook, file_library)

        elif choice == "4":
            # ENCRYPT FILE AFTER USING
            encryption.encrypt_file("library.txt")
            encryption.encrypt_file("borrow_list.txt")
            encryption.encrypt_file("logbook.txt")

            print("\nThank you for using this system. Goodbye!")
            break
        else:
            print("\nInvalid user input. Please select a valid option.")

main_interface() # CALLS THE MAIN INTERFACE FUNCTION