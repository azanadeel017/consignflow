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
    print("--- Scanning for items starting with 'M1' ---")
    
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
            # Get the 'Sale Price' from the current row.
            price = row["Sale Price"]
            
            # Print a clean confirmation statement showing the item name and gross sale price.
            print(f"Match Found! Item: '{title}' | Sale Price: ${price}")
            
            # Increment our counter of matches by 1.
            match_count += 1
            
    # Print a blank line for spacing.
    print()
    # Print the total number of items that matched the 'M1' scan.
    print(f"Total matching items found: {match_count}")
