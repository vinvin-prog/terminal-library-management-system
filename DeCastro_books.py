'''
AMIEL VINCENT V. DE CASTRO
Y6L
'''

import DeCastro_borrow as borrow

# FUNCTION TO LOAD THE LIBRARY
def load_books_from_file(file_library):
    books = {}

    # TRY - ENSURES ANY POTENTIAL ERRORS WHEN OPENING A FILE IS HANDLED
    try:
        with open(file_library, 'r') as file: # WITH - ENSURE FILE IS PROPERLY CLOSED AFTER USING IT
            lines = file.readlines() # READS EACH LINE AND STORES IT IN A LIST NAMED "lines"
            for line in lines:

                parts = line.strip().split(",")

                book_id = parts[0].strip()
                title = parts[1].strip()
                author = parts[2].strip()
                publication_date = parts[3].strip()
                status = parts[4].strip()
                borrowers = parts[5:]

                # CONVERT BORROWERS STRING INTO A LIST
                borrower_list = []
  
                for borrower in borrowers:
                    stripped_borrower = borrower.strip()  # REMOVE EXTRA SPACES
                    if stripped_borrower:
                        borrower_list.append(stripped_borrower)
                
                books[book_id] = {
                    "Title": title,
                    "Author": author,
                    "Publication Date": publication_date,
                    "Status": status,
                    "List of Borrowers": borrower_list
                }

    except FileNotFoundError: # EXCEPT - IF THE FILE DOES NOT YET EXIST, IT INFORMS THE USER THAT A NEW FILE WILL BE CREATED
        print("Error: File does not exist.")

    except ValueError as error: # ERROR HANDLING IF FILE IS CORRUPTED OR RESULTS TO AN ERROR
        print(f"\nError reading the file: {error}. The file might be corrupted or have an unexpected format.")
    
    return books

def save_books_to_file(added_books, file_library):
    with open(file_library, 'w') as file: # OPENS A DATA FILE AND ALLOWS IT TO WRITE IN THE DATA FILE

        for book_id, details in added_books.items():

            borrowers = ','.join(details["List of Borrowers"]) # CONVERT THE LIST OF BORROWERS TO A STRING (A COMMA-SEPARATED LIST).
            file.write(f"{book_id},{details['Title']},{details['Author']},{details['Publication Date']},{details['Status']},{borrowers}\n") # WRITES BOOK DETAILS TO THE DATA FILE

    # print("\nBook/s have been saved to the file.")

def leap_year_checker(year):    
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_days_in_chosen_month(month, year):

    months_31_days = ["Jan", "Mar", "May", "Jul", "Aug", "Oct", "Dec"]
    months_30_days = ["Apr", "Jun", "Sep", "Nov"]

    if month == "Feb":
        if leap_year_checker(year) == True:
            return 29
        else:
            return 28
    elif month in months_31_days:
        return 31
    elif month in months_30_days:
        return 30

def is_valid_day(month, day, year):
    days_in_chosen_month = get_days_in_chosen_month(month, year)

    if day < 1 or day > days_in_chosen_month:
        print(f"\nThe month of {month} in {year} only has {days_in_chosen_month} days.")
        return False
    
    else:
        return True

def title_author_validation(books, title, author):

    new_title = title.lower().strip().replace(" ", "")
    new_author = author.lower().strip().replace(" ", "")
    
    for book_id, details in books.items():
        existing_title = details["Title"].lower().strip().replace(" ", "")
        existing_author = details["Author"].lower().strip().replace(" ", "")
        
        if existing_title == new_title and existing_author == new_author:
            return True
    return False

def publication_date_validation():
    while True:
        publication_year = input("\nEnter book publication year (e.g., 2005, 2023, ...): ").strip()
        
        if publication_year.isdigit():
            year = int(publication_year)
            
            if year < 1000:
                print("\nThe book was published a long time ago. Please enter a valid year.")
            elif year > 2024:
                print("\nInvalid user input. Please enter a valid year.")
            elif publication_year != str(year):
                print("\nInvalid user input. Please enter the year without leading zeros.")
            else:
                if leap_year_checker(year) == True:
                    print(f"\n{year} is a leap year, so February will have 29 days.\n")
                else:
                    print(f"\n{year} is not a leap year, so February will have 28 days.\n")
                break
        else:
            print("\nInvalid user input. Please enter a (positive) numeric value.")

    while True:
        publication_month = input("Enter book publication month (first three letters: Jan-Dec): ").strip().capitalize()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if publication_month not in months:
            print("\nInvalid user input. Please enter a valid month abbreviation.\n")
        else:
            break

    while True:
        publication_day = input("Enter book publication day: ").strip()

        if publication_day.isdigit():
            day = int(publication_day)
            if publication_day != str(day):
                print("\nInvalid user input. Please enter the day without leading zeros.\n")
            elif not is_valid_day(publication_month, day, year):
                print(f"\nInvalid user input. Please enter a valid day.\n")
            else:
                break
        else:
            print("\nInvalid user input. Please enter a valid day.\n")

    validated_date_pub = f"{publication_day} {publication_month} {publication_year}"
    return validated_date_pub

def add_book(library, file_library):
    added_books = library

    while True:
        num_books_to_add = input("\nEnter number of books you wish to add (type 'exit' to go back): ").strip()

        if num_books_to_add.lower() == "exit":
            break
        
        elif num_books_to_add.isdigit():
            num_of_books = int(num_books_to_add)

            if num_of_books > 5:
                print("\nNumber of book(s) to add is too large. Only a maximum 5 books can be added to the library.")
                
            else:
                counter = 0
                while counter < num_of_books:
                    while True:
                        book_title = input("\nBook title: ").strip()
                        book_author = input("Book author: ").strip()

                        book_exists = title_author_validation(added_books, book_title, book_author)

                        if book_exists == True:
                            print("\nThe book already exists in the library.")
                            break

                        publication_date = publication_date_validation()

                        id_numberer = 1
                        
                        while f"B{id_numberer}" in added_books:
                            id_numberer += 1
                        
                        book_id = f"B{id_numberer}"

                        added_books[book_id] = {
                            "Title": book_title, 
                            "Author": book_author, 
                            "Publication Date": publication_date, 
                            "Status": "Available",
                            "List of Borrowers": []}
                        print("\nBook/s successfully added to library!")
                        counter += 1
                        break

                # SAVE BOOKS TO FILE AFTER ALL ADDITION
                save_books_to_file(added_books, file_library)
                break
        else:
            print("\nInvalid user input. Please enter a numeric number (e.g., 1, 2, ...)")

    return added_books

def delete_book(library, file_library):
    if library != {}:

        while True: 
            book_title = input("\nEnter book title you wish to delete (type 'exit' to go back; press 'Enter' key to search all book title): ").strip()

            if book_title.lower() == "exit":
                break
            
            book_author = input("Enter the author of the book (type 'exit' to stop searching; press 'Enter' key to search all book author given book title): ").strip()
            if book_author.lower() == "exit":
                break
            
            books_to_delete = []
            book_exists = False

            find_title = book_title.lower().strip().replace(" ", "")
            find_author = book_author.lower().strip().replace(" ", "")

            for book_id, details in library.items():
                existing_title = details["Title"].lower().strip().replace(" ", "")
                existing_author = details["Author"].lower().strip().replace(" ", "")

                if find_title in existing_title and find_author in existing_author and details["Status"] == "Available": # CHECKS IF USER INPUT IS A SUBSTRING OF A TITLE AND AUTHOR
                    if book_exists == False:
                        print("\nHere are the details of the book/s that can be deleted:")
                    print(f"\nBook ID: {book_id}")
                    print(f"Title: {details['Title']}")
                    print(f"Author: {details['Author']}")
                    print(f"Publication Date: {details['Publication Date']}")
                    print(f"Status: {details['Status']}")
                    print(f"List of Borrowers: {details['List of Borrowers']}")
                    print()
                    print("---" * 15)
                    books_to_delete.append(book_id)
                    book_exists = True

            if book_exists == True:
                while True:
                    book_id_num = input("\nEnter only the ID number of the book you wish to delete (type 'exit' to go back): ").strip()
                        
                    if book_id_num.lower() == "exit":
                        break
                            
                    elif book_id_num.isdigit():
                        book_id_delete = int(book_id_num)
                        find_ID = f"B{book_id_delete}"

                        if book_id_num != str(book_id_delete):
                            print("\nInvalid user input. Please enter a numeric value without leading zeroes.")
    
                        elif find_ID not in books_to_delete:
                            print("\nThe book/s you wish to delete do not have this ID.")
                            continue
                            
                        else:
                            print(f"\nYou are deleting the book with ID: {find_ID}")
                            find_ID_details = library[find_ID]

                            print("\nHere are the details of the book:")
                            print(f"Title: {find_ID_details['Title']}")
                            print(f"Author: {find_ID_details['Author']}")
                            print(f"Publication Date: {find_ID_details['Publication Date']}")
                            print(f"Status: {find_ID_details['Status']}")
                            print(f"List of Borrowers: {find_ID_details['List of Borrowers']}")

                            while True:
                                confirm = input("\nConfirm deletion of the book from the library (y/n): ").lower().strip()
                                
                                if confirm == "y":
                                    del library[find_ID]
                                    print("\nThe book has been successfully deleted from the library.")
                                    book_exists = True
                                    break
                                elif confirm == "n":
                                    print("\nAction canceled.")
                                    book_exists = True
                                    break
                                else:
                                    print("\nInvalid user input.")
                        break

                    else:
                        print("\nInvalid user input. Please enter a numerical value.")
            elif book_exists == False:
                print("\nThere is no book in the library that has this search criteria.")
        
        # SAVE UPDATED LIBRARY AFTER DELETION OF THE BOOK
        save_books_to_file(library, file_library)

    else:
        print("\nThere are currently no books in the library.")

# FUNCTION TO DELETE ALL BOOKS
def delete_all_books(library, file_library):
    if library != {}:
        print("\nBooks that are borrowed will not be deleted.")
        
        while True:
            confirm = input("\nConfirm deletion of all books from the library (y/n): ").lower().strip()
            
            if confirm == "y":

                books_to_delete = []

                for book_id, details in library.items():
                    if details["Status"] == "Available":
                        books_to_delete.append(book_id)

                # DELETE ALL BOOKS FROM LIBRARY EXCEPT FOR BORROWED BOOKS. UPDATE LIBRARY
                for del_book_id in books_to_delete:
                    del library[del_book_id]

                print("\nAll books from library have been deleted except for book(s) that have been borrowed.")
                save_books_to_file(library, file_library)
                break

            elif confirm == "n":
                print("\nAction canceled.")
                break
            
            else:
                print("\nInvalid user input.")
        return
    
    else:
        print("\nThere are currently no books in the library.")

# FUNCTION TO VIEW A BOOK
def view_book(library):
    if library != {}:
        while True:
            find_book = input("\nEnter book title you are looking for (type 'exit' to cancel action; press 'Enter' key to search all book titles): ").strip()

            if find_book.lower() == "exit":
                break

            found = False

            find_title = find_book.lower().strip().replace(" ", "")

            for book_id, details in library.items():
                existing_title = details["Title"].lower().strip().replace(" ", "")
                
                if find_title in existing_title: # CHECKS IF USER INPUT IS A SUBSTRING OF A TITLE
                    
                    # CONVERT LIST OF BORROWERS TO STRING
                    borrowers_list = details["List of Borrowers"]
                    
                    if found == False:
                        print("\nHere are the details of the book/s you are searching for:")
                    print(f"\nBook ID: {book_id}")
                    print(f"Title: {details['Title']}")
                    print(f"Author: {details['Author']}")
                    print(f"Publication Date: {details['Publication Date']}")
                    print(f"Status: {details['Status']}")
                    print(f"List of Borrowers: {borrowers_list}")
                    print()
                    print("---" * 15)
                    found = True

            if found == False:
                print("\nNo book/s found matching your search criteria.")

    else:
        print("\nThere are currently no books in the library.")

# FUNCTION TO EDIT A BOOK
def edit_book(library):
    if library != {}:

        while True:
            edit_book = input("\nEnter part of the title of the book you wish to edit (type 'exit' to go back; press 'Enter' key to search all book titles): ").strip()

            if edit_book.lower() == "exit":
                break
            
            books_to_edit = []
            found = False

            find_title = edit_book.lower().strip().replace(" ", "")

            for book_id, details in library.items():
                existing_title = details["Title"].lower().strip().replace(" ", "")
                
                if find_title in existing_title and details["Status"] == "Available": # CHECKS IF USER INPUT IS A SUBSTRING OF A TITLE
                    if found == False:
                        print("\nHere are the details of the book(s) you can edit:")
                    print(f"\nBook ID: {book_id}")
                    print(f"Title: {details['Title']}")
                    print(f"Author: {details['Author']}")
                    print(f"Publication Date: {details['Publication Date']}")
                    print()
                    print("---" * 15)
                    books_to_edit.append(book_id)
                    found = True
                    
            if found == True:
                while True:
                    book_id_num = input("\nEnter only the ID number of the book you wish to edit (type 'exit' to go back): ").strip()

                    if book_id_num.lower() == "exit":
                        break
                    
                    elif book_id_num.isdigit():
                        book_id_edit = int(book_id_num)
                        find_ID = f"B{book_id_edit}"

                        if book_id_num != str(book_id_edit):
                            print("\nInvalid user input. Please enter a numeric value without leading zeroes.")

                        elif find_ID not in books_to_edit:
                            print("\nThe book/s you wish to edit do not have this ID.")
                        
                        else:
                            print(f"\nYou are editing the book with ID: {find_ID}")
                            find_ID_details = library[find_ID]

                            print("\nHere are the current details of the book:")
                            print(f"Title: {find_ID_details['Title']}")
                            print(f"Author: {find_ID_details['Author']}")
                            print(f"Publication Date: {find_ID_details['Publication Date']}")

                            while True:
                                edit_title = input("\nEnter new title: ").strip()
                                edit_author = input("Enter new author: ").strip()

                                # CHECK IF NEW TITLE AND AUTHOR IS THE SAME
                                new_title = edit_title.lower().strip().replace(" ", "")
                                new_author = edit_author.lower().strip().replace(" ", "")

                                book_edit_title = find_ID_details["Title"].lower().strip().replace(" ", "")
                                book_edit_author = find_ID_details["Author"].lower().strip().replace(" ", "")

                                if new_title == book_edit_title and new_author == book_edit_author:
                                    while True:
                                        confirmation = input("\nRetain the existing title and author (y) or change it (n): ").lower().strip()

                                        if confirmation == "y":
                                            break

                                        elif confirmation == "n":
                                            break

                                        else:
                                            print("\nInvalid user input.")

                                    if confirmation == "y":
                                        break
            
                                else:
                                    book_exists = title_author_validation(library, edit_title, edit_author)

                                    if book_exists == True:
                                        print("\nA book with this title and author exists in the library.")
                                        
                                    elif book_exists == False:
                                        break

                            # GET A NEW PUBLICATION DATE USING THE PUBLICATION DATE VALIDATION
                            new_publication_date = publication_date_validation()
                                
                            while True:
                                # CONFIRMATION OF EDIT
                                confirm = input("\nAre you sure you want to update the details of this book? (y/n): ").lower().strip()

                                if confirm == "y":
                                    # UPDATE DETAILS OF THE BOOK
                                    find_ID_details["Title"] = edit_title
                                    find_ID_details["Author"] = edit_author
                                    find_ID_details["Publication Date"] = new_publication_date

                                    # DISPLAY EDITED BOOK DETAILS
                                    print("\nThe book details have been updated:")
                                    print(f"Updated title: {find_ID_details['Title']}")
                                    print(f"Updated Author: {find_ID_details['Author']}")
                                    print(f"Updated Publication Date: {find_ID_details['Publication Date']}")
                                    break

                                elif confirm == "n":
                                    print("\nAction canceled.")
                                    break

                                else:
                                    print("\nInvalid user input.")

                            break

                    else:
                        print("\nInvalid user input. Please enter a numerical value.")

            elif found == False:
                print("\nTheere are no books in the library that can be edited.")
    else:
        print("\nThere are currently no books in the library.")


def view_pending(borrow_list):
    if borrow_list != {}:

        has_pending = False

        # PRINT ALL PENDING BOOKS TO BE RETURNED
        for borrow_id, borrow_details in borrow_list.items():
            if borrow_details["Status"] == "Unavailable":  
                if has_pending == False:
                    print("\nPending returns:")
                print(f"\nBook ID: {borrow_id}")
                print(f"Title: {borrow_details['Title']}")
                print(f"Author: {borrow_details['Author']}")
                print(f"Date Published: {borrow_details['Publication Date']}")
                print(f"Status: {borrow_details['Status']}")
                print(f"Last Borrower: {borrow_details['Borrower']}")
                print(f"Expected Date of Return: {borrow_details['Date Return']}")
                print()
                print("---" * 15)
                has_pending = True

        if has_pending == False:
            print("\nThere are no pending books to be returned.")

    else:
        print("\nThere are no pending books to be returned.")


# MAIN FUNCTION FOR BOOKS MODULE
def books_module(file_library, file_borrow_list):

    # LOAD LIBRARY FILE AND BORROW LIST FILE
    library = load_books_from_file(file_library)
    borrow_list = borrow.load_borrow_list(file_borrow_list)

    while True:
        print("\n    WELCOME TO THE LIBRARY")
        print("\t[1] Add Book/s")
        print("\t[2] Delete a Book")
        print("\t[3] Delete All Books")
        print("\t[4] View a Book")
        print("\t[5] Edit a Book")
        print("\t[6] View Pending")
        print("\t[7] Go back to Main Menu")
        choice = input("\nEnter option number: ").strip()

        if choice == "1":
            add_book(library, file_library)
        elif choice == "2":
            delete_book(library, file_library)
        elif choice == "3":
            delete_all_books(library, file_library)
        elif choice == "4":
            view_book(library)
        elif choice == "5":
            edit_book(library)
        elif choice == "6":
            view_pending(borrow_list)
        elif choice == "7":
            save_books_to_file(library, file_library)
            return
        else:
            print("\nInvalid user input. Please select a valid option.")