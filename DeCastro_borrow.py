'''
AMIEL VINCENT V. DE CASTRO
Y6L
'''

import DeCastro_books as books
import DeCastro_logbook as logbook

# FUNCTION TO LOAD BORROW LIST FROM FILE
def load_borrow_list(file_borrow_list):
    borrow_list = {}

    # TRY - ENSURES ANY POTENTIAL ERRORS WHEN OPENING A FILE IS HANDLED
    try:
        with open(file_borrow_list, 'r') as file: # WITH - ENSURE FILE IS PROPERLY CLOSED AFTER USING IT
            lines = file.readlines() # READS EACH LINE AND STORES IT IN A LIST NAMED "lines"
            
            if not lines:  # CHECK IF THE FILE IS EMPTY
                return borrow_list # RETURN EMPTY DICTIONARY
            
            for line in lines:

                parts = line.strip().split(",")
                if len(parts) != 9:
                    print(f"Skipping invalid borrow entry: {line.strip()}")
                    continue # SKIP THIS LINE IF IT'S INVALID

                borrow_id, book_id, log_id, date_return, book_title, book_author, book_pub_date, status, person_name = parts

                borrow_list[borrow_id] = {
                    "Book_ID": book_id,
                    "Log_ID": log_id,
                    "Date Return": date_return,
                    "Title": book_title,
                    "Author": book_author,
                    "Publication Date": book_pub_date,
                    "Status": status,
                    "Borrower": person_name,}

    except FileNotFoundError:
        print()

    except ValueError as error: # ERROR HANDLING IF FILE IS CORRUPTED OR RESULTS TO AN ERROR
        print(f"Error reading the file: {error}. The file might be corrupted or have an unexpected format.")
    
    return borrow_list

# FUNCTION TO SAVE BORROW LIST TO FILE
def save_borrow_list(borrow_list, file_borrow_list):
    with open(file_borrow_list, 'w') as file: # OPENS A DATA FILE AND ALLOWS IT TO WRITE IN THE DATA FILE
        
        for borrow_id, details in borrow_list.items():
            file.write(f"{borrow_id},{details['Book_ID']},{details['Log_ID']},{details['Date Return']},{details['Title']},{details['Author']},{details['Publication Date']},{details['Status']},{details['Borrower']}\n")
    
    # print("\nBorrow list entries have been saved to the file.")

# FUNCTION TO VIEW EXPECTED RETURNS
def view_expected_returns(borrow_list):
    
    # ERROR HANDLING IF BORROW LIST IS EMPTY
    if not borrow_list:
        print("\nThere are currently no books borrowed from the library.")
        return
    
    year = 2024 # HARD CODED, NEED IMPORT DATETIME TO BE MORE DYNAMIC AND FLEXIBLE
    
    while True:
        user_date = input("\nEnter the day and month to view expected returns (DD MMM) (or type 'exit' to go back): ").strip()
        if user_date.lower() == "exit":
            return

        try: # TRY - ENSURES ANY POTENTIAL ERRORS WHEN OPENING A FILE IS HANDLED
            
            # SPLIT THE DATE INPUTTED BY THE USER
            user_date_parts = user_date.split(" ")
            day = int(user_date_parts[0])
            month = user_date_parts[1].capitalize()

            month_days = {
                "Jan": 31, "Feb": 28, "Mar": 31, 
                "Apr": 30, "May": 31, "Jun": 30, 
                "Jul": 31, "Aug": 31, "Sep": 30, 
                "Oct": 31, "Nov": 30, "Dec": 7}

            if books.leap_year_checker(year):
                month_days["Feb"] = 29

            if month not in month_days:
                print("\nInvalid month. Please try again.")
                continue
            
            elif month == "Dec" and day > month_days["Dec"]:
                print("\nExpected book returns are only up until December 7.")
                continue

            elif day < 1 or day > month_days[month]:
                print("\nInvalid day for the given month. Please try again.")
                continue

            user_date_formatted = f"{day} {month} {year}"

        except (ValueError, IndexError): # IF THE USER INPUTS A DIFFERENT VALUE OR AN INVALID DATE FORMAT
            print("\nInvalid date format. Please enter the day and month in the format (DD MMM).")
            continue

        found_entries = False

        for borrow_id, details in borrow_list.items():
            if details["Date Return"] == user_date_formatted:
                if found_entries == False:
                    print(f"\nViewing book(s) expected to be returned on {user_date_formatted}:")
                print(f"\nBorrow ID: {borrow_id}")
                print(f"Title: {details['Title']}")
                print(f"Author: {details['Author']}")
                print(f"Date Published: {details['Publication Date']}")
                print(f"Status: {details['Status']}")
                print(f"Borrower: {details['Borrower']}")
                print()
                print("---" * 15)
                found_entries = True
        
        if found_entries == False:
            print(f"\nNo books are due for return on {user_date_formatted}.")
            
        else:
            print("\nExpected book return(s) for the specified date have been displayed.")

# FUNCTION TO VIEW ALL ENTRIES
def view_all_borrow_entries(borrow_list):

    # ERROR HANDLING IF BORROW LIST IS EMPTY
    if not borrow_list:
        print("\nThere are currently no books borrowed from the library.")
        return

    print("\nViewing all borrow entries:")

    for borrow_id, details in borrow_list.items():
        print(f"\nBorrow ID: {borrow_id}")
        print(f"Title: {details['Title']}")
        print(f"Author: {details['Author']}")
        print(f"Date Published: {details['Publication Date']}")
        print(f"Return Date: {details['Date Return']}")
        print(f"Borrower Name: {details['Borrower']}")
        print()
        print("---" * 15)
    
    print("\nAll borrow entries have been displayed.")

# FUNCTION TO RETURN BOOK
def return_book(file_library, borrow_list, file_borrow_list, file_logbook):

    logbook_data = logbook.load_logbook(file_logbook)
    books_data = books.load_books_from_file(file_library)

    # CHECK IF THERE IS AN UNAVAILABLE BOOK
    is_there_unavailable = False
    for book_id, details in books_data.items():
        if details["Status"] == "Unavailable":
            is_there_unavailable = True
            break
    
    if is_there_unavailable == False:
        print("\nThere are no books borrowed. No book(s) will be returned.")
        return

    while True:
        # IF YES, GET USER INFORMATION (Name)
        person_name = input("\nEnter your name (type 'exit' to go back): ").strip()
        
        if person_name.lower() == "exit":
            return
        elif person_name == "":
            print("\nThis is a required field. Please enter your name.")
        else:
            break

    # GET USER INFORMATION (Date, Time, and Purpose using LOGBOOK MODULE)
    # GET CURRENT YEAR
    while True:
        year_inputted = input("\nEnter current year: ").strip()

        if year_inputted.isdigit():
            year = int(year_inputted)

            if year_inputted != str(year):
                print("\nInvalid user input. Please enter year without leading zeroes.")
            elif year != 2024: # STRICTLY LET THE LOGBOOK ENTRY TO BE LOGGED IN 2024
                print("\nInvalid user input. Please enter the current year.")
            else:
                if books.leap_year_checker(year) == True:
                    print(f"\n{year} is a leap year, so February will have 29 days.\n")
                else:
                    print(f"\n{year} is not a leap year, so February will have 28 days.\n")
                break    
        else:
            print("\nInvalid user input. Enter current year.")
    
    # GET MONTH OF LOG
    while True:
        month_inputted = input("Enter month (first three letters: Jan-Dec): ").strip().capitalize()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        if month_inputted not in months:
            print("\nInvalid user input. Please enter a valid month abbreviation.\n")
        else:
            if month_inputted == "Dec":
                print("\nThe library is closed every month of December, but book returns only until December 7 are allowed.\n")
                break
            else:
                break
    
    # GET DAY OF LOG
    while True:
        day_inputted = input("Enter day: ").strip()

        if day_inputted.isdigit():
            day = int(day_inputted)

            if day_inputted != str(day):
                print("\nInvalid user input. Please enter the day without leading zeros.\n")
            elif not books.is_valid_day(month_inputted, day, year):
                print(f"\nInvalid user input. Please enter a valid day.\n")
            elif month_inputted == "Dec":
                if day > 7:
                    print("\nThe library is already closed from December 8 onwards. Book returns will be accepted, but will be given violations based from the library policies on returning borrowed books.")
                    break
                else:
                    break
            else:
                break
        else:
            print("\nInvalid user input. Please enter a valid day.\n")


    date = f"{day_inputted} {month_inputted} {year_inputted}"
    time = logbook.validate_time()
    purpose = "Return"

    # GENERATE UNIQUE LOG ID
    id_numberer = 1

    while f"L{id_numberer}" in logbook_data:
        id_numberer += 1
    
    log_id = f"L{id_numberer}"

    user_borrowed_books = {}
    found_books = False

    for borrow_id, details in borrow_list.items():
        person_name = person_name.lower().strip().replace(" ", "")
        existing_name = details["Borrower"].lower().strip().replace(" ", "")

        if person_name in existing_name:
            user_borrowed_books[borrow_id] = details
            found_books = True

    if found_books == False:
        print(f"\nNo borrowed books found under the name {person_name}.")
        return

    print("\nHere are the details of the book(s) you have borrowed:")
    for borrow_id, details in user_borrowed_books.items():
        print(f"\nBorrow ID: {borrow_id}")
        print(f"Title: {details['Title']}")
        print(f"Author: {details['Author']}")
        print(f"Return Date: {details['Date Return']}")
        print()
        print("---" * 15)

    while True:
        return_book_id = input("\nEnter only the borrow ID number of the book you wish to return (type 'exit' to go back): ").strip()
        if return_book_id.lower() == "exit":
            return logbook_data
                        
        elif return_book_id.isdigit():
            return_book = int(return_book_id)
            find_id = f"BL{return_book}"

            if return_book_id != str(return_book):
                print("\nInvalid user input. Please enter a numeric value without leading zeroes.")

            elif find_id not in user_borrowed_books:
                print("\nThe book(s) you wish to return do not have this borrow ID.")

            else:
                print(f"\nYou are returning the book with borrow ID: {find_id}")
                find_id_details = user_borrowed_books[find_id]

                print("\nHere are the details of the book:")
                print(f"Book ID: {find_id_details['Book_ID']}")
                print(f"Title: {find_id_details['Title']}")
                print(f"Author: {find_id_details['Author']}")
                print(f"Publication Date: {find_id_details['Publication Date']}")

                while True:
                    confirmation = input("\nConfirm return (y/n): ").strip().lower()
                    
                    if confirmation == "y":
                        # SAVE LOGBOOK ENTRY FOR RETURNING BOOKS
                        logbook_data[log_id] = {
                            "Name": person_name,
                            "Date": date,
                            "Time": time,
                            "Purpose": purpose}

                        logbook.save_logbook(logbook_data, file_logbook)

                        # DELETE BOOK FROM BORROW LIST
                        del borrow_list[find_id]
                        save_borrow_list(borrow_list, file_borrow_list)

                        # CHANGE STATUS OF BOOK RETURNED
                        returned_book_id = find_id_details["Book_ID"]
                        books_data[returned_book_id]["Status"] = "Available"
                        books.save_books_to_file(books_data, file_library)

                        print("\nBook has been successfully returned!")
                        return logbook_data, books_data, borrow_list

                    elif confirmation == "n":
                        print("\nBook return canceled.")
                        break
                    
                    else:
                        print("\nInvalid user input.")
        else:
            print("\nInvalid user input. Please enter a numerical value.")

# FUNCTION TO VALIDATE DATE OF RETURN
def validate_return_date(date_borrowed):
    print(f"\nDate Borrowed (Date Logged): {date_borrowed}")
    print("\nIMPORTANT NOTE:\n(1) Books can only be borrowed for a maximum of one week.\n(2) Books can be returned in the month of December.")

    # GET ALL PARTS OF DATE BORROWED
    borrowed_date_parts = date_borrowed.split(" ")
    borrowed_year = int(borrowed_date_parts[2].strip())
    borrowed_day = int(borrowed_date_parts[0].strip())
    borrowed_month = borrowed_date_parts[1].strip().capitalize()

    # DUE TO THE LIBRARY ONLY ALLOWING USERS TO BORROW BOOKS FOR 7 DAYS,
    # DEFINE NUMBER OF DAYS IN EACH MONTH
    month_days = {
        "Jan": 31, "Feb": 28, "Mar": 31, 
        "Apr": 30, "May": 31, "Jun": 30, 
        "Jul": 31, "Aug": 31, "Sep": 30, 
        "Oct": 31, "Nov": 30}

    if books.leap_year_checker(borrowed_year):
        month_days["Feb"] = 29

    # CHECKING FOR THE DUE OF THE BOOK TO BE RETURNED
    must_return_day = borrowed_day + 7

    # IF THE RETURN DAY EXCEEDS THE DAYS IN THE BORROWED MONTH
    if must_return_day > month_days[borrowed_month]:
        must_return_day -= month_days[borrowed_month]

        # BECAUSE IT EXCEEDED NO. OF DAYS OF BORROWED MONTH, MOVE TO THE NEXT MONTH
        ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # FIND THE INDEX OF CURRENT MONTH
        borrowed_month_index = ordered_months.index(borrowed_month)

        #MOVE TO THE NEXT MONTH
        must_return_month = ordered_months[(borrowed_month_index + 1)]

        if must_return_month == "Dec":
            must_return_year = borrowed_year # YEAR WILL NOT CHANGE
        else:
            must_return_year = borrowed_year
    
    else:
        must_return_month = borrowed_month
        must_return_year = borrowed_year
    
    print(f"\nThe borrowed book must be returned no later than: {must_return_day} {must_return_month} {must_return_year}")

    # GET RETURN DATE FROM THE USER
    return_year = must_return_year
    while True:
        user_return = input("\nEnter return day and month (DD MMM): ").strip()
        
        try: # TRY - ENSURES ANY POTENTIAL ERRORS WHEN OPENING A FILE IS HANDLED
            
            # SPLIT THE RETURN DAY AND MONTH INPUTTED BY THE USER
            user_return_parts = user_return.split(" ")
            return_day = int(user_return_parts[0])
            return_month = user_return_parts[1].capitalize()

            ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            if ordered_months.index(return_month) < ordered_months.index(borrowed_month):
                print("\nThe return date cannot be earlier than the borrowed date.")
            
            elif return_month == borrowed_month and return_day < borrowed_day:
                print("\nThe return date cannot be earlier than the borrowed date.")
            
            elif return_month == borrowed_month and return_day == borrowed_day:
                print("\nThe return date cannot be the same as the borrowed date.")

            elif ordered_months.index(return_month) > ordered_months.index(must_return_month):
                print("\nThe return date is past the allowed 7-day borrowing period.")
            
            elif return_month == must_return_month and return_day > must_return_day:
                print("\nThe return date is past the allowed 7-day borrowing period.")

            elif return_month == "Dec":
                return_date = f"{return_day} {return_month} {return_year}"
                return return_date

            else:
                return_date = f"{return_day} {return_month} {return_year}"
                return return_date

        except (ValueError, IndexError): # IF THE USER INPUTS A DIFFERENT VALUE OR AN INVALID DATE FORMAT
            print("\nInvalid date format. Please enter the return day and month in the format (DD MMM).")

# FUNCTION TO BORROW BOOK
def borrow_book(file_library, borrow_list, file_borrow_list, file_logbook):

    logbook_data = logbook.load_logbook(file_logbook)
    books_data = books.load_books_from_file(file_library)

    # CHECK IF THERE ARE AVAILABLE BOOKS THAT CAN BE BORROWED
    is_there_available = False
    for book_Id, details in books_data.items():
        if details["Status"] == "Available":
            is_there_available = True
            break
    
    if is_there_available == False:
        print("\nAll books in the library are currently unavailable. Come back again.")
        return

    while True:
        # GET USER INFORMATION (Name)
        person_name = input("\nEnter your name (type 'exit' to go back): ").strip()

        if person_name.lower() == "exit":
            return
        elif person_name == "":
            print("\nThis is a required field. Please enter your name.")
        else:
            break

    # GET USER INFORMATION (Date, Time, and Purpose using LOGBOOK MODULE)
    date = logbook.validate_date()

    if date == "Dec":
        return

    time = logbook.validate_time()
    purpose = "Borrow"

    # GENERATE UNIQUE LOG ID
    id_numberer = 1

    while f"L{id_numberer}" in logbook_data:
        id_numberer += 1
    
    log_id = f"L{id_numberer}"

    # GET BOOK INFORMATION FROM THE USER
    book_title = input("\nEnter the book title (type 'exit' to cancel borrow; press 'Enter' key to search all book title): ").strip()
    if book_title.lower() == "exit":
        return

    book_author = input("Enter the book author (type 'exit' to cancel borrow; press 'Enter' key to search all book author given book title): ").strip()
    if book_author.lower() == "exit":
        return

    books_to_borrow = []
    book_exists = False

    borrow_title = book_title.lower().strip().replace(" ", "")
    borrow_author = book_author.lower().strip().replace(" ", "")

    for book_id, details in books_data.items():
        existing_title = details["Title"].lower().strip().replace(" ", "")
        existing_author = details["Author"].lower().strip().replace(" ", "")

        if borrow_title in existing_title and borrow_author in existing_author and details["Status"] == "Available":
            if book_exists == False:
                print("\nHere are the details of the book(s) available for borrowing:")
            print(f"\nBook ID: {book_id}")
            print(f"Title: {details['Title']}")
            print(f"Author: {details['Author']}")
            print(f"Publication Date: {details['Publication Date']}")
            print()
            print("---" * 15)
            books_to_borrow.append(book_id)
            book_exists = True
    
    if book_exists == True:
        while True:
            book_id_num = input("\nEnter only the ID number of the book you wish to borrow (type 'exit' to go back): ").strip()
                        
            if book_id_num.lower() == "exit":
                break
                            
            elif book_id_num.isdigit():
                book_id_borrow = int(book_id_num)
                find_id = f"B{book_id_borrow}"

                if book_id_num != str(book_id_borrow):
                    print("\nInvalid user input. Please enter a numeric value without leading zeroes.")
    
                elif find_id not in books_to_borrow:
                    print("\nThere is no book(s) that has this ID.")
                            
                else:
                    print(f"\nYou are borrowing the book with ID: {find_id}")
                    find_id_details = books_data[find_id]

                    print("\nHere are the details of the book:")
                    print(f"Title: {find_id_details['Title']}")
                    print(f"Author: {find_id_details['Author']}")
                    print(f"Publication Date: {find_id_details['Publication Date']}")

                    date_borrowed = date
                    date_return = validate_return_date(date_borrowed)

                    # CREATE LOGBOOK ENTRY
                    logbook_data[log_id] = {
                        "Name": person_name,
                        "Date": date,
                        "Time": time,
                        "Purpose": purpose}

                    logbook.save_logbook(logbook_data, file_logbook)

                    borrow_id_numberer = 1

                    while True:
                        borrow_id = f"BL{borrow_id_numberer}"

                        # CHECK IF THE BORROW ID IS ALREADY IN THE BORROW LIST
                        is_borrow_id_in_list = borrow_id in borrow_list

                        # CHECK IF THE BORROW ID IS IN THE "LIST OF BORROWERS" FOR ANY BOOK
                        is_borrow_id_in_books = False
                        for book in books_data.values():
                            if borrow_id in book.get("List of Borrowers", []):
                                is_borrow_id_in_books = True
                                break
                        
                        # IF THE BORROW ID IS NOT FOUND IN BOTH PLACES, IT'S UNIQUE.
                        if not is_borrow_id_in_list and not is_borrow_id_in_books:
                            break

                         # IF THE BORROW ID ALREADY EXISTS, INCREMENT THE NUMBER AND TRY AGAIN
                        borrow_id_numberer += 1

                    borrow_list[borrow_id] = {
                        "Book_ID": find_id,
                        "Log_ID": log_id,
                        "Date Return": date_return,
                        "Title": find_id_details['Title'],
                        "Author": find_id_details['Author'],
                        "Publication Date": find_id_details['Publication Date'],
                        "Status": "Unavailable",
                        "Borrower": person_name,}
                    
                    # SAVE TO BORROW LIST
                    save_borrow_list(borrow_list, file_borrow_list)

                    # UPDATE BOOK BORROWED STATUS IN LIBRARY DICTIONARY
                    books_data[find_id]["Status"] = "Unavailable"

                    # APPEND THE (NEW) BORROW_ID TO THE (EXISTING) LIST OF BORROWERS
                    if "List of Borrowers" not in books_data[find_id]:
                        books_data[find_id]["List of Borrowers"] = []

                    if borrow_id not in books_data[find_id]["List of Borrowers"]:
                        books_data[find_id]["List of Borrowers"].append(borrow_id)

                    books.save_books_to_file(books_data, file_library)

                    print("\nThe book has been successfully borrowed.")
                    return borrow_list, logbook_data, books_data

            else:
                print("\nInvalid user input. Please enter a numerical value.")

    elif book_exists == False:
        print("\nThere is no book in the library that has this search criteria.")

# FUNCTION TO DISPLAY BORROW MODULE MENU
def borrow_module(file_library, file_borrow_list, file_logbook):

    borrow_list = load_borrow_list(file_borrow_list)

    while True:
        print("\n    LIBRARY BORROW MENU")
        print("\t[1] Borrow Book")
        print("\t[2] Return Book")
        print("\t[3] View All Borrow Entries")
        print("\t[4] View Expected Returns")
        print("\t[5] Go back to Main Menu")
        choice = input("\nEnter option number: ").strip()

        if choice == "1":
            borrow_book(file_library, borrow_list, file_borrow_list, file_logbook)
        elif choice == "2":
            return_book(file_library, borrow_list, file_borrow_list, file_logbook)
        elif choice == "3":
            view_all_borrow_entries(borrow_list)
        elif choice == "4":
            view_expected_returns(borrow_list)
        elif choice == "5":
            save_borrow_list(borrow_list, file_borrow_list)
            return
        else:
            print("\nInvalid user input. Please select a valid option.")