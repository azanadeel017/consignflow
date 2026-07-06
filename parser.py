# Import the built-in 'csv' module to read and write CSV files.
import csv
# Import the built-in 'os' module to handle system file paths.
import os

# Get the directory where this script is located.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the CSV file relative to this script's directory.
csv_path = os.path.join(script_dir, "mock_sales.csv")

# Print a friendly message to show we are starting the scan.
print(f"Reading sales data from: {csv_path}\n")

# Open the CSV file. 'r' stands for read mode, and we use utf-8 encoding.
with open(csv_path, mode="r", encoding="utf-8") as file:
    # Use DictReader to parse each row of the CSV as a dictionary.
    # The header row ('Item Title', 'Sale Price', 'Platform') will be the keys.
    reader = csv.DictReader(file)
    
    # Initialize a counter to keep track of how many matching items we find.
    match_count = 0
    
    # Print a header for the results output.
    print("--- Scanning for items starting with 'M1' & Calculating Payouts ---\n")
    
    # Loop through each row of the CSV file one by one.
    for row in reader:
        # Get the 'Item Title' from the current row.
        title = row["Item Title"]
        
        # Clean the title defensively:
        # 1. strip() removes any leading or trailing spaces (e.g. " M1 " -> "M1").
        # 2. lower() converts all letters to lowercase (e.g. "M1" -> "m1").
        cleaned_title = title.strip().lower()
        
        # Check if the cleaned title starts with the prefix "m1".
        if cleaned_title.startswith("m1"):
            # Get the 'Sale Price' from the current row and convert it to a float number for calculations.
            gross_price = float(row["Sale Price"])
            
            # Calculate the Whatnot marketplace flat commission (8% of gross sale price).
            commission = round(gross_price * 0.08, 2)
            
            # Calculate the Whatnot transaction fee (2.9% of gross sale price).
            transaction_fee = round(gross_price * 0.029, 2)
            
            # Define the flat fee per item of $0.30.
            flat_fee = 0.30
            
            # Add up all the individual fees to get the total marketplace fee.
            total_fees = round(commission + transaction_fee + flat_fee, 2)
            
            # Subtract total fees from gross price to determine final payout for the seller.
            net_payout = round(gross_price - total_fees, 2)
            
            # Print a detailed, clean confirmation summary showing gross price, fees breakdown, and net payout.
            print(f"Match Found! Item: '{title}'")
            print(f"  Gross Price:  ${gross_price:.2f}")
            print(f"  Whatnot Fees: ${total_fees:.2f} (8% Commission: ${commission:.2f} | 2.9% Tx Fee: ${transaction_fee:.2f} | Flat Fee: ${flat_fee:.2f})")
            print(f"  Net Payout:   ${net_payout:.2f}\n")
            
            # Increment our counter of matches by 1.
            match_count += 1
            
    # Print the total number of items that matched the 'M1' scan.
    print(f"Total matching items found: {match_count}")
