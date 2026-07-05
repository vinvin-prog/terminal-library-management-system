'''
AMIEL VINCENT V. DE CASTRO
Y6L
'''

import DeCastro_books as books

# FUNCTION TO LOGBOOK FROM FILE
def load_logbook(file_logbook):
    logbook = {}

    # TRY - ENSURES ANY POTENTIAL ERRORS WHEN OPENING A FILE IS HANDLED
    try:
        with open(file_logbook, 'r') as file: # WITH - ENSURE FILE IS PROPERLY CLOSED AFTER USING IT
            lines = file.readlines() # READS EACH LINE AND STORES IT IN A LIST NAMED "lines"
            for line in lines:

                parts = line.strip().split(",")
                if len(parts) != 5:
                    continue  # SKIP THIS LINE IF IT'S INVALID

                log_id, person_name, date, time, purpose = parts

                if not lines:  # CHECK IF THE FILE IS EMPTY
                    print("The logbook file is empty.")
                    return logbook # RETURN EMPTY DICTIONARY

                logbook[log_id] = {
                    "Name": person_name,
                    "Date": date,
                    "Time": time,
                    "Purpose": purpose
                }

    except FileNotFoundError: # EXCEPT - IF THE FILE DOES NOT YET EXIST, IT INFORMS THE USER THAT A NEW FILE WILL BE CREATED
        print()

    except ValueError as error: # ERROR HANDLING IF FILE IS CORRUPTED OR RESULTS TO AN ERROR
        print(f"Error reading the file: {error}. The file might be corrupted or have an unexpected format.")

    return logbook

# FUNCTION TO SAVE LOGBOOK FILE
def save_logbook(logbook, file_logbook):
    with open(file_logbook, 'w') as file: # OPENS A DATA FILE AND ALLOWS IT TO WRITE IN THE DATA FILE

        for log_id, details in logbook.items():
            file.write(f"{log_id},{details['Name']},{details['Date']},{details['Time']},{details['Purpose']}\n")

    # print("\nLogbook entries have been saved to the file.")


# FUNCTION TO VALIDATE USER INPUT FOR THE DATE INPUT FIELD
def validate_date():
    
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
        month_inputted = input("Enter month (first three letters: Jan-Nov): ").strip().capitalize()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        if month_inputted not in months:
            print("\nInvalid user input. Please enter a valid month abbreviation.\n")
        elif month_inputted == "Dec":
            print("\nSorry, the library is closed every month of December. Only book returns are allowed during this month. Thank you for understanding!")
            break
        else:
            break
    
    # LIBRARY IS CLOSED
    if month_inputted == "Dec":
        return "Dec"
    
    # GET DAY OF LOG
    while True:
        day_inputted = input("Enter day: ").strip()

        if day_inputted.isdigit():
            day = int(day_inputted)

            if day_inputted != str(day):
                print("\nInvalid user input. Please enter the day without leading zeros.\n")
            elif not books.is_valid_day(month_inputted, day, year):
                print(f"\nInvalid user input. Please enter a valid day.\n")
            else:
                break
        else:
            print("\nInvalid user input. Please enter a valid day.\n")
    
    validated_date = f"{day_inputted} {month_inputted} {year_inputted}"
    print(f"\nDate logged: {validated_date}")

    return validated_date

# FUNCTION TO VALIDATE USER INPUT FOR THE TIME INPUT FIELD
def validate_time():
    
    print("\nFollowing the 12-hour clock format:")
    
    # GET THE CURRENT HOUR
    while True:
        input_hour = input("\nEnter hour in the current time (1-12): ").strip()
        if input_hour.isdigit():
            hour = int(input_hour)
            if input_hour != str(hour):
                print("\nInvalid user input. Please enter the hour without leading zeroes.")
            elif hour < 1 or hour > 12:
                print("\nInvalid user input. Please enter the hour following the 12-hour clock format.")
            else:
                break
        else:
            print("\nInvalid user input. Please enter a valid hour.")

    # GET THE CURRENT MINUTE
    while True:
        input_minute = input("\nEnter minute in the current time (00-59): ").strip()
        if input_minute.isdigit():
            minute = int(input_minute)

            if minute >= 1 and minute <= 9:
                string_minute = str(minute)
                converted_string_minute = f"0{string_minute}"
                input_minute = converted_string_minute
                break

            elif minute > 59:
                print("\nInvalid user input. Please enter a valid minute.")

            else:
                break
        
        else:
            print("\nInvalid user input. Please enter a valid minute.")
    
    # DETERMINE WHETHER AM OR PM
    while True:
        input_am_pm = input("\nEnter AM or PM: ").strip().upper()

        if input_am_pm == "AM" or input_am_pm == "PM":
            break

        else:
            print("\nInvalid user input. Please enter whether 'AM' or 'PM.'")
    
    validated_time = f"{input_hour}:{input_minute} {input_am_pm}"
    print(f"\nTime logged: {validated_time}")

    return validated_time

# FUNCTION TO VALIDATE USER INPUT FOR THE PURPOSE INPUT FIELD
def validate_purpose(library):

    while True:
        valid_purpose = ["borrow", "return", "visit"]
        purpose = input("\nEnter purpose (borrow/return/visit): ").strip().lower()

        # IF USER INPUT IS CORRECT
        if purpose in valid_purpose:

            # IF "BORROW"
            if purpose == "borrow":
                if not library:
                    print("\nThe library is currently empty. There are no books that can be borrowed.")
                    return False
                else:
                    is_there_available = False
                    for book_id, details in library.items():
                        if details["Status"] == "Available":
                            is_there_available = True
                            break

                    if is_there_available == False:
                        print("\nAll books in the library are currently unavailable. Come back again.")
                        return False
                    
                    elif is_there_available == True:
                        return purpose.capitalize()
            
            # IF "RETURN"
            if purpose == "return":
                if not library:
                    print("\nThe library is empty. No book(s) expected to be returned to the library.")
                    return False
                else:
                    is_there_unavailable = False
                    for book_id, details in library.items():
                        if details["Status"] == "Unavailable":
                            is_there_unavailable = True
                            break

                    if is_there_unavailable == False:
                        print("\nThere are no books borrowed. No book(s) will be returned.")
                        return False
                    
                    elif is_there_unavailable == True:
                        return purpose.capitalize()

            else:
                return purpose.capitalize()
        
        # IF USER INPUT IS INCORRECT
        else:
            print("\nInvalid user input. Please enter 'borrow', 'return', or 'visit'.")

# FUNCTION TO ADD LOG ENTRY OF USER
def add_log_entry(logbook, file_logbook, library):

    added_logs = logbook

    # GET USER INFORMATION
    person_name = input("\nEnter name (type 'exit' to go back): ").strip()

    if person_name.lower() == "exit":
        return added_logs

    date = validate_date()

    if date == "Dec":
        return added_logs

    time = validate_time()
    purpose = validate_purpose(library)

    if purpose == False:
        return

    # GENERATE UNIQUE LOG ID
    id_numberer = 1

    while f"L{id_numberer}" in added_logs:
        id_numberer += 1
    
    log_id = f"L{id_numberer}"

    # ADD ALL INFORMATION TO LOGBOOK DICTIONARY
    added_logs[log_id] = {
        "Name": person_name,
        "Date": date,
        "Time": time,
        "Purpose": purpose}
    print("\nYou have successfully logged!")
    save_logbook(added_logs, file_logbook)

# FUNCTION TO VIEW ALL LOG ENTRIES
def view_all_entries(logbook):
    if logbook != {}:
        print("\nHere are all the existing logbook entries:")

        # PRINT ALL LOG ENTRIES
        for log_id, details in logbook.items():
            print(f"\nLog ID: {log_id}")
            print(f"Person Name: {details['Name']}")
            print(f"Date: {details['Date']}")
            print(f"Time: {details['Time']}")
            print(f"Purpose: {details['Purpose']}")
            print()
            print("---" * 15)

    else:
        print("\nThe logbook is currently empty.")

# FUNCTION TO VIEW ALL ENTRIES GIVEN A SPECIFIED DATE
def view_entries_by_date(logbook):
    if logbook != {}:
        while True:
            find_log_date = validate_date()

            if find_log_date == "Dec":
                continue

            found_entries = False
            
            for log_id, details in logbook.items():
                if details["Date"] == find_log_date:
                    if found_entries == False:
                        print("\nHere are all logbook entries that match the date stated:")
                    print(f"\nLog ID: {log_id}")
                    print(f"Person Name: {details['Name']}")
                    print(f"Date: {details['Date']}")
                    print(f"Time: {details['Time']}")
                    print(f"Purpose: {details['Purpose']}")
                    print()
                    print("---" * 15)
                    found_entries = True

            if found_entries == False:
                print("\nThere are no entries found for the specified date.")
            
            while True:
                continue_search = input("\nContinue searching (y) or exit search (n): ").strip().lower()

                if continue_search == "y":
                    break
                elif continue_search == "n":
                    return
                else:
                    print("\nInvalid user input.")
    else:
        print("\nThe logbook is currently empty.")

# MAIN FUNCTION FOR LOGBOOK MODULE
def logbook_module(file_logbook, file_library):

    # LOAD LOGBOOK FILE
    logbook = load_logbook(file_logbook)
    library = books.load_books_from_file(file_library)

    while True:
        print("\n    LIBRARY LOGBOOK")
        print("\t[1] Add Log Entry")
        print("\t[2] View All Entries")
        print("\t[3] View Transactions by Date")
        print("\t[4] Go back to Main Menu")
        choice = input("\nEnter option number: ").strip()

        if choice == "1":
            add_log_entry(logbook, file_logbook, library)
        elif choice == "2":
            view_all_entries(logbook)
        elif choice == "3":
            view_entries_by_date(logbook)
        elif choice == "4":
            save_logbook(logbook, file_logbook)
            return
        else:
            print("\nInvalid user input. Please select a valid option.")