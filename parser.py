# Import the built-in 'csv' module to read and write CSV files.
import csv
# Import the built-in 'os' module to handle system file paths.
import os
# Import ABC and abstractmethod to define interface classes (Strategy Pattern).
from abc import ABC, abstractmethod

class FeeCalculator(ABC):
    """
    Abstract Base Class defining the interface for all marketplace fee calculators.
    This demonstrates the Strategy Design Pattern for cleaner, object-oriented code.
    """
    @abstractmethod
    def calculate_fees(self, gross_price: float) -> dict:
        """
        Abstract method that subclasses must implement to calculate fees.
        Returns a dictionary with 'commission', 'transaction_fee', 'flat_fee', and 'total_fees'.
        """
        pass


class WhatnotFeeCalculator(FeeCalculator):
    """
    Fee calculator strategy specifically for Whatnot.
    Whatnot charges: 8% commission, 2.9% transaction fee, and $0.30 flat fee.
    """
    def calculate_fees(self, gross_price: float) -> dict:
        commission = round(gross_price * 0.08, 2)
        transaction_fee = round(gross_price * 0.029, 2)
        flat_fee = 0.30
        total_fees = round(commission + transaction_fee + flat_fee, 2)
        return {
            "commission": commission,
            "transaction_fee": transaction_fee,
            "flat_fee": flat_fee,
            "total_fees": total_fees
        }


class EbayFeeCalculator(FeeCalculator):
    """
    Fee calculator strategy specifically for eBay (Collectibles/Clothing category).
    eBay charges: 13.25% commission and $0.30 flat fee per order/item.
    """
    def calculate_fees(self, gross_price: float) -> dict:
        commission = round(gross_price * 0.1325, 2)
        transaction_fee = 0.0  # Included in final value fee
        flat_fee = 0.30
        total_fees = round(commission + flat_fee, 2)
        return {
            "commission": commission,
            "transaction_fee": transaction_fee,
            "flat_fee": flat_fee,
            "total_fees": total_fees
        }


class PoshmarkFeeCalculator(FeeCalculator):
    """
    Fee calculator strategy specifically for Poshmark.
    Poshmark charges:
    - Under $15.00: flat commission of $2.95.
    - $15.00 and over: 20% of Gross.
    """
    def calculate_fees(self, gross_price: float) -> dict:
        if gross_price < 15.0:
            commission = 2.95
        else:
            commission = round(gross_price * 0.20, 2)
        transaction_fee = 0.0
        flat_fee = 0.0
        total_fees = round(commission, 2)
        return {
            "commission": commission,
            "transaction_fee": transaction_fee,
            "flat_fee": flat_fee,
            "total_fees": total_fees
        }


class TikTokShopFeeCalculator(FeeCalculator):
    """
    Fee calculator strategy specifically for TikTok Shop.
    TikTok Shop charges: 6% commission and $0.30 flat fee.
    """
    def calculate_fees(self, gross_price: float) -> dict:
        commission = round(gross_price * 0.06, 2)
        transaction_fee = 0.0
        flat_fee = 0.30
        total_fees = round(commission + flat_fee, 2)
        return {
            "commission": commission,
            "transaction_fee": transaction_fee,
            "flat_fee": flat_fee,
            "total_fees": total_fees
        }


class FeeCalculatorFactory:
    """
    Factory class to fetch the correct FeeCalculator instance based on the platform name.
    """
    # Registry of supported calculators. Standardized to lowercase keys.
    _registry = {
        "whatnot": WhatnotFeeCalculator(),
        "ebay": EbayFeeCalculator(),
        "poshmark": PoshmarkFeeCalculator(),
        "tiktok shop": TikTokShopFeeCalculator(),
        "tiktokshop": TikTokShopFeeCalculator()
    }

    @classmethod
    def get_calculator(cls, platform: str) -> FeeCalculator:
        # Standardize the platform key to lowercase and strip extra spacing
        key = platform.strip().lower()
        if key in cls._registry:
            return cls._registry[key]
        else:
            # Fall back to a default calculator or raise an informative error
            raise ValueError(f"Unsupported platform: '{platform}'")


# Get the directory where this script is located.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the CSV file relative to this script's directory.
csv_path = os.path.join(script_dir, "mock_sales.csv")

# Print a friendly message to show we are starting the scan.
print(f"Reading sales data from: {csv_path}\n")

# Open the CSV file. 'r' stands for read mode, and we use utf-8 encoding.
with open(csv_path, mode="r", encoding="utf-8") as file:
    # Use DictReader to parse each row of the CSV as a dictionary.
    reader = csv.DictReader(file)
    
    # Initialize a counter to keep track of how many matching items we find.
    match_count = 0
    
    # Print a header for the results output.
    print("--- Scanning for items starting with 'M1' & Calculating Multi-Platform Payouts ---\n")
    
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
            # Get the platform name from the row.
            platform = row["Platform"]
            
            # Get the 'Sale Price' and convert it to float for calculations.
            gross_price = float(row["Sale Price"])
            
            try:
                # Retrieve the appropriate fee calculator using the Factory.
                calculator = FeeCalculatorFactory.get_calculator(platform)
                
                # Calculate the breakdown of fees.
                fees = calculator.calculate_fees(gross_price)
                
                commission = fees["commission"]
                transaction_fee = fees["transaction_fee"]
                flat_fee = fees["flat_fee"]
                total_fees = fees["total_fees"]
                
                # Subtract total fees from gross price to determine final payout for the seller.
                net_payout = round(gross_price - total_fees, 2)
                
                # Print a detailed, clean confirmation summary showing gross price, platform, fees breakdown, and net payout.
                print(f"Match Found! Item: '{title}'")
                print(f"  Platform:     {platform}")
                print(f"  Gross Price:  ${gross_price:.2f}")
                print(f"  Fees Charged: ${total_fees:.2f} (Commission: ${commission:.2f} | Tx Fee: ${transaction_fee:.2f} | Flat Fee: ${flat_fee:.2f})")
                print(f"  Net Payout:   ${net_payout:.2f}\n")
                
                # Increment our counter of matches by 1.
                match_count += 1
                
            except ValueError as e:
                # Handle cases where the platform is not yet supported.
                print(f"Warning! Match Found but Skipped: '{title}'")
                print(f"  Error: {e}\n")
                
    # Print the total number of items that matched the 'M1' scan.
    print(f"Total matching items found: {match_count}")
