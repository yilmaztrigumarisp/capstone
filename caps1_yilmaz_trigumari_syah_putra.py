from prettytable import PrettyTable
from tabulate import tabulate

# Data kendaraan berat dengan data dummy
vehicles = [
    {
        "Vehicle Number": "HDT-HO-54",
        "Vehicle Type": "Dump Truck",
        "Status": "Available",
        "Operating Hours": 10.0,
        "Downtime Hours": 1.0,
        "Idle Hours": 1.0
    },
    {
        "Vehicle Number": "HX-SA3-01",
        "Vehicle Type": "Excavator",
        "Status": "Breakdown",
        "Operating Hours": 4.0,
        "Downtime Hours": 7.0,
        "Idle Hours": 1.0
    },
    {
        "Vehicle Number": "HF-HE3-12",
        "Vehicle Type": "Forklift",
        "Status": "Available",
        "Operating Hours": 8.0,
        "Downtime Hours": 3.0,
        "Idle Hours": 1.0
    }
]

# Fungsi untuk menghitung indikator produktivitas alat berat
def vehicle_indicators(operating_hours, downtime_hours, idle_hours):
    total_time = operating_hours + downtime_hours + idle_hours
    if total_time == 0:
        return 0, 0, 0, 0 # bertujuan untuk mencegah pembagian dengan angka 0

    physical_availability = ((operating_hours + idle_hours) / total_time) * 100
    mechanical_availability = (operating_hours / (operating_hours + downtime_hours)) * 100 if (operating_hours + downtime_hours) > 0 else 0
    utilization_availability = (operating_hours / (operating_hours + idle_hours)) * 100 if (operating_hours + idle_hours) > 0 else 0
    effective_utilization = (operating_hours / total_time) * 100

    return physical_availability, mechanical_availability, utilization_availability, effective_utilization

# Fungsi untuk menampilkan semua data kendaraan dalam bentuk tabel
def overall_table_data():
    if not vehicles:
        print(
            "No vehicles in the system."
            )
        return

    table = PrettyTable()
    table.field_names = [
        "Vehicle No", "Vehicle Type", "Status", "Operating Hours", "Downtime Hours", "Idle Hours"
        ]
    
    for vehicle in vehicles:
        table.add_row([
            vehicle["Vehicle Number"].upper(),
            vehicle["Vehicle Type"],
            vehicle["Status"],
            vehicle["Operating Hours"],
            vehicle["Downtime Hours"],
            vehicle["Idle Hours"]
        ])
    print(table)
    
    sort_choice = confirm_yes_no("Do you want to sort the table? (yes/no): ")
    if sort_choice == 'yes':
        sort_table()
    else:
            print("Data has not been sorted.")

# Fungsi untuk menampilkan indikator produktivitas kendaraan tertentu
def display_productivity_indicators():
    vehicle_number = input("Enter Vehicle Number to view productivity indicators: ").upper()
    found = False
    for vehicle in vehicles:
        if vehicle["Vehicle Number"] == vehicle_number:
            found = True
            pa, ma, ua, eu = vehicle_indicators(
                vehicle["Operating Hours"], vehicle["Downtime Hours"], vehicle["Idle Hours"]
            )
            table = PrettyTable()
            table.field_names = ["Vehicle No", "PA (%)", "MA (%)", "UA (%)", "EU (%)"]
            table.add_row([vehicle["Vehicle Number"].upper(), f"{pa:.2f}", f"{ma:.2f}", f"{ua:.2f}", f"{eu:.2f}"])
            print(table)
            break
    if not found:
        print("Vehicle not found.")

# Fungsi untuk menampilkan data bedasarkan tabel
def display_spesific_data():
    vehicle_number = input_vehicle_number("Enter Vehicle Number to retrieve: ")
    for vehicle in vehicles:
        if vehicle["Vehicle Number"] == vehicle_number:
            table = PrettyTable()
            table.field_names = ["Vehicle No", "Type", "Status", "Operating Hrs", "Downtime Hrs", "Idle Hrs"]
            table.add_row([
                vehicle["Vehicle Number"],
                vehicle["Vehicle Type"],
                vehicle["Status"],
                vehicle["Operating Hours"],
                vehicle["Downtime Hours"],
                vehicle["Idle Hours"]
            ])
            print(table)
            return 
    
    print("Vehicle not found.")

# Fungsi untuk menyortir tabel berdasarkan kolom dan urutan(bubble sort)
def sort_table():
    header = ["Vehicle Number", "Vehicle Type", "Status", "Operating Hours", "Downtime Hours", "Idle Hours"]
    column = input(f"Choose a column to sort by (options: {', '.join(header)}): ").strip().title()
    if column not in header:
        print("Invalid column. Please try again.")
        return

    sort_order = input("Choose sorting order (ascending or descending): ").strip().lower()
    if sort_order not in ['ascending', 'asc', 'descending', 'desc']:
        print("Invalid sorting order. Please try again.")
        return
    
    column_key = column 
    n = len(vehicles)
    for i in range(n):
        for j in range(0, n - i - 1):
            
            if sort_order == 'ascending' or 'asc':
                if vehicles[j][column_key] > vehicles[j + 1][column_key]:
                    vehicles[j], vehicles[j + 1] = vehicles[j + 1], vehicles[j]
            else:
                if vehicles[j][column_key] < vehicles[j + 1][column_key]:
                    vehicles[j], vehicles[j + 1] = vehicles[j + 1], vehicles[j]

    table = PrettyTable()
    table.field_names = header
    for vehicle in vehicles:
        table.add_row([vehicle[key] for key in header])

    print(f"\nTable sorted by '{column}' in '{sort_order}' order.")
    print(table)
    
# Fungsi untuk meminta input konfirmasi 'yes' atau 'no' saja
def confirm_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ["yes", "no"]:
            return choice
        print("Invalid input. Please enter 'yes' or 'no'.")

# Fungsi untuk validasi bagian jenis alat berat
def input_vehicle_type(prompt):
    while True:
            vehicle_type = input("Enter Vehicle Type (ex: Excavator, Dump Truck, etc.): ").strip().lower()
            if vehicle_type in ["excavator", "forklift", "dump truck", "loader", "trailer", "light truck", "bulldozer"]:
                vehicle_type = vehicle_type.capitalize()
                return vehicle_type
            print("Invalid input. Please input one of the 7 heavy equipment types.")

# Fungsi untuk validasi bagian status alat berat
def input_status(prompt):
    while True:
            status = input("Enter Status (Available or Breakdown): ").strip().lower()
            if status in ["available", "breakdown"]:
                status = status.capitalize()
                return status
            print("Invalid input. Please input 'Available' or 'Breakdown' only.")

# Fungsi untuk meminta input nomor kendaraan valid (kombinasi huruf dan angka)
def input_vehicle_number(prompt):
    while True:
        value = input(prompt).strip()
        if value.replace("-", "").isalnum():  # fungsi replace untuk menghilangkan tanda "-" sementara untuk ngebypass validasi while true
            return value.upper()
        print("Invalid input. Vehicle number must be a combination of letters and numbers.")

# Fungsi untuk meminta input float yang valid (hanya angka desimal yang diizinkan)
def input_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# Submenu untuk menambahkan data kendaraan baru
def create_sub_menu():
    while True:
        vehicle_type_table = [
            ["1", "Excavator (ex: HX-SA3-01)"],
            ["2", "Dump Truck (ex: HDT-HO-01)"],
            ["3", "Forklift (ex: HF-HE3-01)"],
            ["4", "Loader (ex: HWL-XC-01)"],
            ["5", "Trailer (ex: HPM-HO-01)"],
            ["6", "Light Truck (ex: HLT-MF-01)"],
            ["7", "Bulldozer (ex: HD-SH-01)"],
            ["8", "Exit to Main Menu"]
        ]

        print("\n======= Heavy Equipment Addition Sub Menu =======\n")
        print(tabulate(vehicle_type_table, headers=["Option", "Vehicle Type"], tablefmt="pipe"))

        choice = input("\nChoose a vehicle type to add (1-8): ")

        if choice == '1':  
            vehicle_type = "Excavator"
            try:
                weight_capacity = int(input("Enter a vehicle weight number code (ex: input 3 for HX-SA3): "))
                number = int(input("Enter vehicle number (ex: input 16 for HX-SA3-16): "))
                vehicle_number = (f"HX-SA{weight_capacity}-{number:02d}")
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '2':  
            vehicle_type = "Dump Truck"
            try:
                number = int(input("Enter vehicle number (ex: input 54 for HDT-HO-54): "))
                vehicle_number = (f"HDT-HO-{number:02d}")
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '3':  
            vehicle_type = "Forklift"
            try:
                weight_capacity = int(input("Enter a vehicle weight number code (ex: input 3 for HF-HE3): "))
                number = int(input("Enter vehicle number (ex: input 12 for HF-HE3-12): "))
                vehicle_number = f"HF-HE{weight_capacity}-{number:02d}"
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '4':  
            vehicle_type = "Loader"
            try:
                number = int(input("Enter vehicle number (ex: input 22 for HWL-XC-22): "))
                vehicle_number = f"HWL-XC-{number:02d}"
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '5':  
            vehicle_type = "Trailer"
            try:
                number = int(input("Enter vehicle number (ex: input 10 for HPM-HO-10): "))
                vehicle_number = f"HPM-HO-{number:02d}"
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '6':  
            vehicle_type = "Light Truck"
            try:
                number = int(input("Enter vehicle number (ex: input 8 for HLT-MF-08): "))
                vehicle_number = f"HLT-MF-{number:02d}"
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '7':  
            vehicle_type = "Bulldozer"
            try:
                weight_capacity = int(input("Enter a vehicle weight number code (ex: input 3 for HD-SH3): "))
                number = int(input("Enter vehicle number (ex: input 5 for HD-SH3-05): "))
                vehicle_number = f"HD-SH{weight_capacity}-{number:02d}"
            except ValueError:
                print("Invalid input. Please input a number.")
                continue

        elif choice == '8':  
            break

        else:
            print("Invalid option. Please choose between 1-8.")
            continue

        if any(vehicle["Vehicle Number"] == vehicle_number for vehicle in vehicles):
            print(f"Duplicate vehicle number {vehicle_number} found. Returning to Create Sub Menu.")
            continue

        status = input_status("Enter Status (Available or Breakdown): ")
        operating_hours = input_float("Enter Operating Hours: ")
        downtime_hours = input_float("Enter Downtime Hours: ")
        idle_hours = input_float("Enter Idle Hours: ")

        new_vehicle = {
            "Vehicle Number": vehicle_number,
            "Vehicle Type": vehicle_type,
            "Status": status,
            "Operating Hours": operating_hours,
            "Downtime Hours": downtime_hours,
            "Idle Hours": idle_hours
        }

        save = confirm_yes_no("Do you want to save this vehicle? (yes/no): ")
        if save == 'yes':
            vehicles.append(new_vehicle)
            print(f"\nVehicle {vehicle_number} ({vehicle_type}) added successfully.")
        else:
            print("Data not saved. Returning to Create Sub Menu.")
        
# Submenu untuk membaca data alat berat
def read_sub_menu():
    while True:
        read_submenu_table = [
            ["1", "Display All Heavy Equipment Data"],
            ["2", "Display a Specific Heavy Equipment Data"],
            ["3", "Display Productivity Indicators"],
            ["4", "Exit to Main Menu"]
        ]

        print("\n======= Heavy Equipment Display Sub Menu =======\n")
        print(tabulate(read_submenu_table, headers=["Option", "List of Sub Menu"], tablefmt="pipe"))

        choice = input("\nChoose an option (1-4): ")

        if choice == '1':
            overall_table_data()
        elif choice == '2':
            display_spesific_data()
        elif choice == '3':
            display_productivity_indicators()
        elif choice == '4':
            break
        else:
            print("Invalid option. Choose '1' to '4'.")

# Submenu untuk memperbarui data kendaraan yang ada (tanpa mengizinkan perubahan nomor kendaraan)
def update_sub_menu():
    while True:
        update_submenu_table = [
            ["1", "Heavy Equipment Update"],
            ["2", "Exit to Main Menu"]
        ]
        print("\n======= Heavy Equipment Report Update Sub Menu =======\n")
        print(tabulate(update_submenu_table, headers=["Option", "List of Sub Menu"], tablefmt="pipe"))

        choice = input("\nChoose an option (1-2): ")

        if choice == '1':
            vehicle_number = input_vehicle_number("Enter Vehicle Number to update (ex: HX-SA3-01, HF-HE3-12): ")
            for vehicle in vehicles:
                if vehicle["Vehicle Number"] == vehicle_number:
                    print(f"\nCurrent data for Vehicle Number {vehicle['Vehicle Number']}:")
                    vehicle["Vehicle Type"] = input_vehicle_type("Enter new Vehicle Type (ex: Excavator, Dump Truck, etc.): ")
                    vehicle["Status"] = input_status("Enter new Status (Available or Breakdown): ")
                    vehicle["Operating Hours"] = input_float("Enter new Operating Hours: ")
                    vehicle["Downtime Hours"] = input_float("Enter new Downtime Hours: ")
                    vehicle["Idle Hours"] = input_float("Enter new Idle Hours: ")

                    save = confirm_yes_no("Save changes? (yes/no): ")
                    if save == 'yes':
                        print("Data updated successfully.")
                    else:
                        print("Changes discarded.")
                    break
            else:
                print("Vehicle not found.")
        elif choice == '2':
            break
        else:
            print("Invalid option. Choose '1' or '2'.")

# Submenu untuk menghapus data kendaraan
def delete_sub_menu():
    while True:
        delete_menu_table = [
            ["1", "Heavy Equipment Deletion"],
            ["2", "Exit to Main Menu"]
        ]

        print("\n======= Heavy Vehicle Data Deletion Sub Menu =======\n")
        print(tabulate(delete_menu_table, headers=["Option", "List of Sub Menu"], tablefmt="pipe"))

        choice = input("\nChoose an option (1-2): ")

        if choice == '1':
            vehicle_number = input_vehicle_number("Enter Vehicle Number to delete (ex: HX-SA3-01, HF-HE3-12): ")
            index = None
            for i, vehicle in enumerate(vehicles):
                if vehicle["Vehicle Number"] == vehicle_number:
                    index = i
                    break
            
            if index is not None:
                delete = confirm_yes_no(f"Are you sure you want to delete Vehicle {vehicle_number.upper()}? (yes/no): ")
                if delete == 'yes':
                    vehicles.pop(index)
                    print(f"Vehicle {vehicle_number.upper()} deleted successfully.")
                else:
                    print("Deletion canceled. Returning to Delete Sub Menu.")
            else:
                print("Vehicle not found. Returning to Delete Sub Menu.")
        elif choice == '2':
            break
        else:
            print("Invalid option. Choose '1' or '2'.")

# Fungsi menu utama
def main_menu():
    while True:
        menu_data = [
            ["1", "Add Heavy Equipment"],
            ["2", "View and Sort Heavy Equipment Data"],
            ["3", "Update Heavy Equipment Data"],
            ["4", "Delete Heavy Equipment Data"],
            ["5", "Exit"]
        ]

        print("\n======= Fleet Management System Menu =======\n")
        print(tabulate(menu_data, headers=["Option", "List of Menu"], tablefmt="pipe"))

        choice = input("\nChoose an option (1-5): ")

        if choice == '1':
            create_sub_menu()
        elif choice == '2':
            read_sub_menu() 
        elif choice == '3':
            update_sub_menu() 
        elif choice == '4':
            delete_sub_menu() 
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose between 1-5.")

# Menjalankan Menu Utama
main_menu()