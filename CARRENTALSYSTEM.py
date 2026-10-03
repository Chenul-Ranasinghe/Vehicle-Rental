import mysql.connector
import datetime
import os
import time
import sys

try:
    if sys.platform == 'win32':
        os.system('')
except:
    pass

# --- COLOR DEFINITIONS ---
RED = '\033[1;31;1m'
GREEN = '\033[1;32;1m'
YELLOW = '\033[1;33;1m '
BLUE = '\033[1;34;1m'
MAGENTA = '\033[1;35;1m'
CYAN = '\033[1;36;1m '
WHITE = '\033[1;37;1m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

TITLE = MAGENTA + BOLD  
HEADER = CYAN + BOLD    
SUCCESS = GREEN         
ERROR = RED             
WARNING = YELLOW        
INPUT = WHITE + BOLD
DATA = WHITE
BORDER = GREEN          

width = 80

# --- DATABASE CONNECTION ---
try:
    mycon = mysql.connector.connect(
        host="localhost",
        user="root",
        password="enter your password here",
        database="car_rental",
        charset="utf8"
    )
    cursor = mycon.cursor()
except Exception as e:
    print(ERROR + "MySQL Error: " + str(e) + END)
    SystemExit()

# --- HELPER FUNCTIONS ---
def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls')

def header(title):
    """
    Displays a formatted header with the given title.
    """
    print(BORDER + "\n" + "*"*width + END + "\n")
    print(TITLE + "CAPPA CAR RENTALS".center(width) + END)
    print(WARNING + " Al Rai, Block 4 | +965 2200 4455".center(width) + "\n")
    print(BORDER + "*"*width + END + '\n')
    print(HEADER + title.center(width) + END)
    print()

def pause():
    """
    Pauses program execution until user presses Enter.
    """
    input(WARNING + "\n\n\n\nPress Enter to continue..." + END)
    

def validate_string(prompt, letters_only=False):
    """
    Validates and returns a string input from the user.
    """
    while True:
        print(WARNING + " " + prompt + ":" + INPUT, end=" ")
        value = input().strip()
        if value == "":
            print(ERROR + " Cannot be empty" + END)
        elif letters_only and (not value.replace(" ", "").isalpha()):
            print(ERROR + " Only letters allowed" + END)
        else:
            return value
        

def validate_int(prompt):
    """
    Validates and returns a positive integer input from the user.
    """
    while True:
        print(WARNING + " " + prompt + ":" + INPUT, end=" ")
        value = input()
        if value.isdigit():
            val = int(value)
            if val <= 0:
                print(ERROR + " Enter positive number" + END)
            else:
                return val
        else:
            print(ERROR + " Enter valid number" + END)
            

def validate_float(prompt):
    """
    Validates and returns a positive float input from the user.
    """
    while True:
        try:
            print(WARNING + " " + prompt + ":" + INPUT, end=" ")
            val = float(input())
            if val <= 0:
                print(ERROR + " Enter positive value" + END)
            else:
                return val
        except:
            print(ERROR + " Enter valid number" + END)
            

def display_table(data, columns):
    """
    Displays tabular data in a formatted table.
    """
    if not data:
        print(WARNING + "\n No data found" + END)
        return
        
    # Calculate column widths
    col_widths = [len(col) + 2 for col in columns]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)) + 2)
    
    # Print header
    print()
    header_line = "  ".join([columns[i].ljust(col_widths[i]) for i in range(len(columns))])
    print("  " + header_line)
    print(BORDER + "  " + "-" * (sum(col_widths) + len(columns) - 1) + END)
    
    # Print data
    for row in data:
        row_line = "  ".join([str(row[i]).ljust(col_widths[i]) for i in range(len(row))])
        print("  " + row_line)
    
    print(BORDER + "  " + "-" * (sum(col_widths) + len(columns) - 1) + END)
    print("\n Total records: " + str(len(data)))
    

# --- ADMIN FUNCTIONS ---
def admin_login():
    """
    Handles admin authentication process.
    """
    header("ADMIN LOGIN")
    print(WARNING + " Username:" + INPUT, end=" ")
    user = input()
    print(WARNING + " Password:" + INPUT, end=" ")
    pswd = input()
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (user, pswd))
    data = cursor.fetchone()
    if data:
        print(SUCCESS + "\n Login successful!" + END)
        pause()
        admin_menu()
    else:
        print(ERROR + "\n Invalid credentials!" + END)
        pause()


def admin_menu():
    """
    Displays and handles the admin dashboard menu.
    """
    while True:
        header("ADMIN PANEL")
        print(BLUE + " 1. Add Vehicle")
        print(" 2. View All Vehicles") 
        print(" 3. Update Vehicle Rent")
        print(" 4. Remove Vehicle")
        print(" 5. Staff Signup")
        print(" 6. Remove Staff")
        print(" 7. View All Rentals")
        print(" 8. View All Customers")
        print(" 9. Logout" + END)
        print(WARNING + "\nEnter choice (1-9):" + INPUT, end=" ")
        choice = input()
        
        if choice == "1":
            add_vehicle()
        elif choice == "2":
            view_all_vehicles()
        elif choice == "3":
            update_vehicle_rent()
        elif choice == "4":
            remove_vehicle()
        elif choice == "5":
            staff_signup()
        elif choice == "6":
            remove_staff()
        elif choice == "7":
            view_all_rentals()
        elif choice == "8":
            view_all_customers()
        elif choice == "9":
            break
        else:
            print(ERROR + " Invalid choice!" + END)
            

def add_vehicle():
    """
    Adds a new vehicle to the rental system database.
    """
    header("ADD NEW VEHICLE")
    plate = validate_string("Plate Number").upper()
    
    cursor.execute("SELECT * FROM vehicles WHERE license_plate=%s", (plate,))
    if cursor.fetchone():
        print(ERROR + "\n Vehicle with this plate already exists!" + END)
        pause()
        return

    make = validate_string("Vehicle Make", letters_only=True)
    model = validate_string("Vehicle Model")
    color = validate_string("Color", letters_only=True)
    year = validate_int("Manufacturing Year")
    rate = validate_float("Daily Rental Rate")

    print(CYAN + "\n Confirm Details:" + END)
    print(DATA + "   Plate: " + plate + " | Make: " + make + " | Model: " + model + END)
    print(DATA + "   Color: " + color + " | Year: " + str(year) + " | Rate: KWD " + str(rate) + END)
    
    print(WARNING + "\n Add this vehicle? (Y/N):" + INPUT, end=" ")
    confirm = input().upper()
    
    if confirm != "Y":
        print(WARNING + "\n Cancelled!" + END)
        pause()
        return

    try:
        cursor.execute("INSERT INTO vehicles (make, model, year, color, license_plate, daily_rate, status) VALUES (%s,%s,%s,%s,%s,%s,'available')",
                       (make, model, year, color, plate, rate))
        mycon.commit()
        print(SUCCESS + "\n Vehicle added successfully!" + END)
    except Exception as e:
        mycon.rollback()
        print(ERROR + " Error: " + str(e) + END)
    pause()
    

def view_all_vehicles():
    """
    Displays all vehicles in the rental system.
    """
    header("ALL VEHICLES")
    cursor.execute("SELECT vehicle_id, make, model, year, color, license_plate, daily_rate, status FROM vehicles")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Make", "Model", "Year", "Color", "Plate", "Rent", "Status"])
    else:
        print(WARNING + "\n No vehicles found" + END)
    pause()
    

def update_vehicle_rent():
    """
    Updates the daily rental rate of a vehicle.
    """
    header("UPDATE VEHICLE RENT")
    cursor.execute("SELECT vehicle_id, make, model, year, color, license_plate, daily_rate, status FROM vehicles")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Make", "Model", "Year", "Color", "Plate", "Rent", "Status"])
        vehicle_id = validate_int("\n Vehicle ID to update")
        cursor.execute("SELECT status FROM vehicles WHERE vehicle_id=%s", (vehicle_id,))
        vehicle = cursor.fetchone()
    
    if not vehicle:
        print(ERROR + "\n Vehicle not found!" + END)
        pause()
        return
    
    if vehicle[0] == 'rented':
        print(ERROR + "\n Cannot update rented vehicle!" + END)
        pause()
        return
    
    new_rate = validate_float(" New daily rent")
    cursor.execute("UPDATE vehicles SET daily_rate=%s WHERE vehicle_id=%s", (new_rate, vehicle_id))
    mycon.commit()
    print(SUCCESS + "\n Rent updated successfully!" + END)
    pause()
    

def remove_vehicle():
    """
    Removes a vehicle from the rental system.
    """
    header("REMOVE VEHICLE")
    cursor.execute("SELECT vehicle_id, make, model, year, color, license_plate, daily_rate, status FROM vehicles")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Make", "Model", "Year", "Color", "Plate", "Rent", "Status"])
        vehicle_id = validate_int("\n Vehicle ID to Delete")
        cursor.execute("SELECT status FROM vehicles WHERE vehicle_id=%s", (vehicle_id,))
        vehicle = cursor.fetchone()
        
    if not vehicle:
        print(ERROR + "\n Vehicle not found!" + END)
        pause()
        return
    
    if vehicle[0] == 'rented':
        print(ERROR + " Cannot remove rented vehicle!" + END)
        pause()
        return
    
    print(WARNING + "\n Confirm deletion? (Y/N):" + INPUT, end=" ")
    confirm = input().upper()
    if confirm == "Y":
        cursor.execute("DELETE FROM vehicles WHERE vehicle_id=%s", (vehicle_id,))
        mycon.commit()
        print(SUCCESS + "\n Vehicle removed!" + END)
    else:
        print(WARNING + "\n Cancelled!" + END)
    pause()
    

def staff_signup():
    """
    Registers a new staff member in the system.
    """
    header("USER SIGNUP")
    username = validate_string("Username")
    password = validate_string("Password")
    full_name = validate_string("Full Name", letters_only=True)
    email = validate_string("Email")
    
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        print(ERROR + " Username already exists!" + END)
        pause()
        return
    
    try:
        cursor.execute("INSERT INTO users (username, password, full_name, email) VALUES (%s,%s,%s,%s)",
                       (username, password, full_name, email))
        mycon.commit()
        print(SUCCESS + " User created successfully!" + END)
    except Exception as e:
        mycon.rollback()
        print(ERROR + " Error: " + str(e) + END)
    pause()
    

def remove_staff():
    """
    Removes a staff member from the system.
    """
    header("REMOVE USER")
    cursor.execute("SELECT user_id, username, full_name FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("\n No users found")
        pause()
        return
    
    display_table(users, ["ID", "Username", "Full Name"])
    user_id = validate_int("\n\n User ID to remove")
    
    # Check if user exists
    cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
    if not cursor.fetchone():
        print("\n User not found!")
        pause()
        return
    
    # Check for active rentals
    cursor.execute("SELECT COUNT(*) FROM rentals WHERE user_id=%s AND status='active'", (user_id,))
    active_count = cursor.fetchone()[0]
    
    if active_count > 0:
        print("\n Cannot remove user! They have " + str(active_count) + " active rental(s).")
        pause()
        return
    
    # Ask for confirmation
    confirm = input("\n Confirm deletion? (Y/N): ").upper()
    
    if confirm != "Y":
        print("\n Operation cancelled!")
        pause()
        return
    
    try:
        cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
        mycon.commit()
        
        # Check if deletion was successful
        if cursor.rowcount > 0:
            print("\n User removed successfully!")
        else:
            print("\n User could not be removed. Please try again.")
    except Exception as e:
        mycon.rollback()
        print(" Error: " + str(e))
    
    pause()
    

def view_all_rentals():
    """
    Displays all rental transactions in the system.
    """
    header("ALL RENTALS")
    cursor.execute("SELECT rental_id, customer_id, vehicle_id, user_id, rental_date, return_date, total_days, total_cost, status FROM rentals")
    data = cursor.fetchall()
    if data:
        display_table(data, ["Rental ID", "Cust ID", "Veh ID", "User ID", "Rental Date", "Return Date", "Days", "Total", "Status"])
    else:
        print(WARNING + " No rentals found" + END)
    pause()
    

def view_all_customers():
    """
    Displays all registered customers in the system.
    """
    header("ALL CUSTOMERS")
    cursor.execute("SELECT customer_id, full_name, email, phone, license_number FROM customers")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Full Name", "Email", "Phone", "License"])
    else:
        print(WARNING + " No customers found" + END)
    pause()


# --- USER FUNCTIONS ---
def staff_login():
    """
    Handles staff member authentication.
    """
    header("USER LOGIN")
    print(WARNING + " Username:" + INPUT, end=" ")
    username = input()
    print(WARNING + " Password:" + INPUT, end=" ")
    password = input()
    
    cursor.execute("SELECT user_id, username, full_name FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        print(SUCCESS + "\n Welcome " + user[2] + "!" + END)
        pause()
        user_menu(user[0])
    else:
        print(ERROR + "\n Invalid credentials!" + END)
        pause()
        

def user_menu(user_id):
    """
    Displays and handles the staff member dashboard menu.
    """
    while True:
        header("USER DASHBOARD")
        print(BLUE + "1. View Available Vehicles")
        print("2. Rent Vehicle") 
        print("3. Return Vehicle")
        print("4. View My Rentals")
        print("5. Logout" + END)
        print(WARNING + "\n Enter choice (1-5):" + INPUT, end=" ")
        choice = input()

        if choice == "1":
            view_available_vehicles()
        elif choice == "2":
            rent_vehicle(user_id)
        elif choice == "3":
            return_vehicle(user_id)
        elif choice == "4":
            view_my_rentals(user_id)
        elif choice == "5":
            break
        else:
            print(ERROR + " Invalid choice!" + END)

def view_available_vehicles():
    """
    Displays all vehicles currently available for rental.
    """
    header("AVAILABLE VEHICLES")
    cursor.execute("SELECT vehicle_id, make, model, year, color, license_plate, daily_rate FROM vehicles WHERE status='available'")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Make", "Model", "Year", "Color", "Plate", "Daily Rent"])
    else:
        print(WARNING + "\n No vehicles available" + END)
    pause()
    

def rent_vehicle(user_id):
    """
    Handles the vehicle rental process.
    """
    header("RENT VEHICLE")
    cursor.execute("SELECT vehicle_id, make, model, year, color, license_plate, daily_rate FROM vehicles WHERE status='available'")
    data = cursor.fetchall()
    if data:
        display_table(data, ["ID", "Make", "Model", "Year", "Color", "Plate", "Daily Rent"])
        vehicle_id = validate_int("\n Vehicle ID to rent")
        cursor.execute("SELECT vehicle_id, daily_rate FROM vehicles WHERE vehicle_id=%s AND status='available'", (vehicle_id,))
        vehicle = cursor.fetchone()
    
    if not vehicle:
        print(ERROR + "\n Vehicle not available!" + END)
        pause()
        return
    
    customer_id = get_or_create_customer()
    if not customer_id:
        return
    
    days = validate_int(" Number of rental days")
    total_cost = vehicle[1] * days
    
    print(CYAN + "\n Total Cost: KWD " + str(total_cost) + END)
    print(WARNING + "\n Confirm rental? (Y/N):" + INPUT, end=" ")
    confirm = input().upper()
    
    if confirm == "Y":
        try:
            rental_date = datetime.datetime.now()
            cursor.execute("INSERT INTO rentals (customer_id, vehicle_id, user_id, rental_date, total_days, total_cost, status) VALUES (%s, %s, %s, %s, %s, %s, 'Active')",
                          (customer_id, vehicle_id, user_id, rental_date, days, total_cost))
            
            cursor.execute("UPDATE vehicles SET status='rented' WHERE vehicle_id=%s", (vehicle_id,))
            mycon.commit()
            print(SUCCESS + "\n Vehicle rented successfully!" + END)
        except Exception:
            mycon.rollback()
            print(ERROR + " Error: Invalid Vehicle ID" + END)
    else:
        print(WARNING + "\n Rental cancelled!" + END)
    pause()
    

def get_or_create_customer():
    """
    Manages customer selection or creation for rentals.
    """
    print(CYAN + "\n Customer Information:" + END)
    print(BLUE + "1. Use existing customer")
    print("2. Create new customer" + END)
    print(WARNING + " Enter choice (1-2):" + INPUT, end=" ")
    choice = input()
    
    if choice == "1":
        return select_existing_customer()
    elif choice == "2":
        return create_new_customer()
    else:
        print(ERROR + "\n Invalid choice!" + END)
        return None
    

def select_existing_customer():
    """
    Allows selection of an existing customer from the database.
    """
    view_all_customers()
    customer_id = validate_int(" Customer ID")
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id=%s", (customer_id,))
    customer = cursor.fetchone()
    if customer:
        return customer[0]
    else:
        print(ERROR + "\n Customer not found!" + END)
        return None
    

def create_new_customer():
    """
    Creates a new customer record in the database.
    """
    header("NEW CUSTOMER")
    full_name = validate_string(" Full Name", letters_only=True)
    email = validate_string(" Email")
    phone = validate_string(" Phone")
    address = validate_string(" Address")
    license_number = validate_string(" License Number")
    
    try:
        cursor.execute("INSERT INTO customers (full_name, email, phone, address, license_number) VALUES (%s, %s, %s, %s, %s)",
                      (full_name, email, phone, address, license_number))
        mycon.commit()
        customer_id = cursor.lastrowid
        print(SUCCESS + "\n Customer created successfully!" + END)
        return customer_id
    except Exception as e:
        mycon.rollback()
        print(ERROR + " Error: " + str(e) + END)
        return None
    

def return_vehicle(user_id):
    """
    Handles vehicle return process.
    """
    header("RETURN VEHICLE")
    cursor.execute("SELECT rental_id, vehicle_id, rental_date FROM rentals WHERE user_id=%s AND status='Active'", (user_id,))
    active_rentals = cursor.fetchall()
    
    if not active_rentals:
        print(WARNING + "\n No active rentals found!" + END)
        pause()
        return
    
    display_table(active_rentals, ["Rental ID", "Vehicle ID", "Rental Date"])
    
    rental_id = validate_int("Rental ID to return")
    return_date = datetime.datetime.now()
    
    try:
        cursor.execute("UPDATE rentals SET return_date=%s, status='returned' WHERE rental_id=%s", (return_date, rental_id))
        
        cursor.execute("SELECT vehicle_id FROM rentals WHERE rental_id=%s", (rental_id,))
        vehicle_id = cursor.fetchone()[0]
        cursor.execute("UPDATE vehicles SET status='available' WHERE vehicle_id=%s", (vehicle_id,))
        mycon.commit()
        print(SUCCESS + "\n Vehicle returned successfully!" + END)

        print(CYAN + "\n Receipt Options:" + END)
        print(BLUE + "  1. Print receipt")
        print("  2. Skip receipt" + END)
        print(WARNING + " Choose option (1-2):" + INPUT, end=" ")
        receipt_choice = input()
        
        if receipt_choice == "1":
            cursor.execute("""
                SELECT 
                    r.rental_id, r.rental_date, r.return_date, r.total_days, r.total_cost,
                    c.full_name, c.license_number, c.phone,
                    v.make, v.model, v.year, v.color, v.license_plate, v.daily_rate,
                    u.full_name as agent_name
                FROM rentals r
                JOIN customers c ON r.customer_id = c.customer_id
                JOIN vehicles v ON r.vehicle_id = v.vehicle_id
                JOIN users u ON r.user_id = u.user_id
                WHERE r.rental_id = %s
            """, (rental_id,))
            
            rental_data = cursor.fetchone()
            
            if rental_data:
                (rental_id, rental_date, return_date, total_days, total_cost,
                 customer_name, license_number, customer_phone,
                 vehicle_make, vehicle_model, vehicle_year, vehicle_color, license_plate, daily_rate,
                 agent_name) = rental_data
                
                header("CAR RENTAL RECEIPT")
                print(DATA + "\tReceipt #: " + str(rental_id) + END)
                print(DATA + "\tDate: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + END)
                print(BORDER + "-"*50 + END)
                print(DATA + "\tCustomer: " + customer_name + END)
                print(DATA + "\tLicense: " + license_number + END)
                print(DATA + "\tPhone: " + customer_phone + END)
                print(BORDER + "-"*50 + END)
                print(DATA + "\tVehicle: " + str(vehicle_year) + " " + vehicle_make + " " + vehicle_model + END)
                print(DATA + "\tColor: " + vehicle_color + END)
                print(DATA + "\tPlate: " + license_plate + END)
                print(BORDER + "-"*50 + END)
                print(DATA + "\tRental Date: " + rental_date.strftime('%Y-%m-%d') + END)
                print(DATA + "\tReturn Date: " + return_date.strftime('%Y-%m-%d') + END)
                print(DATA + "\tDays: " + str(total_days) + END)
                print(DATA + "\tDaily Rate: KWD " + str(daily_rate) + END)
                print(BORDER + "-"*50 + END)
                print(SUCCESS + "\tTOTAL: KWD " + str(total_cost) + END)
                print(BORDER + "-"*50 + END)
                print(CYAN + "\tThank you for your business!" + END)
                print(DATA + "\tCAPPA CAR RENTALS" + END)
                print(DATA + "\tAl Rai, Block 4, Kuwait" + END)
                print(DATA + "\tContact: +965 2200 4455" + END)
                print(DATA + "\tContact: capparentals@gmail.com" + END)
                print(BORDER + "="*50 + END)
                print(SUCCESS + "\n Receipt printed successfully!" + END)
            else:
                print(ERROR + " Could not generate receipt - rental data not found." + END)
        elif receipt_choice == "2":
            print()
            print(CYAN + "\tThank you for your business!" + END)
            print(DATA + "\tCAPPA CAR RENTALS" + END)
            print(DATA + "\tAl Rai, Block 4, Kuwait" + END)
            print(DATA + "\tContact: +965 2200 4455" + END)
            print(DATA + "\tContact: capparentals@gmail.com" + END)
    except Exception as e:
        mycon.rollback()
        print(ERROR + " Error: " + str(e) + END)
    pause()
    

def view_my_rentals(user_id):
    """
    Displays rental history for a specific staff member.
    """
    header("MY RENTALS")
    cursor.execute("SELECT rental_id, vehicle_id, rental_date, return_date, total_days, total_cost, status FROM rentals WHERE user_id=%s", (user_id,))
    data = cursor.fetchall()
    if data:
        display_table(data, ["Rental ID", "Vehicle ID", "Rental Date", "Return Date", "Days", "Total", "Status"])
    else:
        print(WARNING + "\n No rentals found" + END)
    pause()
    

# --- INTRO & MAIN MENU ---
def intro():
    """
    Displays the animated introduction screen.
    """
    clear_screen()
    print("\n" + BORDER + "*" * width + END)
    print("\n" * 5)
    print(TITLE + "W E L C O M E   T O ".center(width) + '\n\n' + "C A P P A   C A R   R E N T A L S".center(width) + END)
    print(WARNING + "\n\n" + " Location: Al Rai, Block 4, Kuwait".center(width))
    print(" Contact: +965 2200 4455".center(width))
    print(" Contact: capparentals@gmail.com".center(width))
    print("\n" * 5 + " Developed By: Chenul".center(width) + END)
    print("\n" + BORDER + "*" * width + END)
    print('\n')
    time.sleep(1)
    
    text = "STARTING SYSTEM"
    print(RED + BOLD + "\t\t" + " " * 15, end="\n\n\t\t\t\t\t\t\t  ")
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.1)
    print("......." + END)
    print()
    
    time.sleep(1)
    input(WARNING + "\n Press Enter to begin..." + END)
    clear_screen()

def main_menu():
    """
    Displays and handles the main system menu.
    """
    while True:
        header("MAIN MENU")
        print(RED + " 1. Admin Login")
        print(" 2. Staff Login") 
        print(" 3. Exit System" + END)
        print(WARNING + "\nEnter your choice (1-3):" + INPUT, end=" ")
        choice = input()
        print('\n' + BORDER + "="*width + END)
        print('\n\n')

        if choice == "1":
            admin_login()
        elif choice == "2":
            staff_login()
        elif choice == "3":
            print("\n\n\n\n" + "*" * width)
            print("\n\n\n" + "Thank you for using Car Rental System!".center(width))
            print("Visit us: Al Rai, Block 4, Kuwait".center(width))
            print("Call: +965 2200 4455".center(width) + "\n\n\n")
            print("*" * width + "\n\n\n\n")
            time.sleep(5)            
            break
        else:
            print(ERROR + " Invalid choice! Please try again." + END)
            pause()

if __name__ == "__main__":
    """
    Main program entry point.
    """
    try:
        intro()
        main_menu()
    except KeyboardInterrupt:
        print("\n\n\t" + WARNING + "Program interrupted by user" + END)
    except Exception as e:
        print("\n\t" + ERROR + "An error occurred: " + str(e) + END)
    finally:
        if 'conn' in locals() and mycon.is_connected():
            cursor.close()
            mycon.close()
            print("\n\n\n\t" + SUCCESS + "Database connection closed." + END)