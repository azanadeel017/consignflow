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


def load_and_parse_sales(csv_file_or_path) -> dict:
    """
    Helper function to load either a CSV file path (string/PathLike) or a file-like object (StringIO),
    filter items starting with 'M1', calculate fees, and aggregate financial statistics.
    Returns a dictionary containing raw matched items list and aggregated stats.
    """
    matched_items = []
    aggregate_gross = 0.0
    aggregate_fees = 0.0
    aggregate_net = 0.0
    platform_breakdown = {}

    # Duck-typing: If it has a 'read' attribute, it's a file-like stream object (e.g. StringIO from Streamlit)
    if hasattr(csv_file_or_path, "read"):
        file = csv_file_or_path
        is_path = False
    else:
        # Otherwise, assume it's a file path string or os.PathLike object
        is_path = True
        try:
            if not os.path.exists(csv_file_or_path):
                return {
                    "items": [],
                    "totals": {"gross": 0.0, "fees": 0.0, "net": 0.0, "count": 0, "margin": 0.0},
                    "platforms": {}
                }
            file = open(csv_file_or_path, mode="r", encoding="utf-8")
        except TypeError:
            # Fallback in case an unsupported type fails disk checking operations
            return {
                "items": [],
                "totals": {"gross": 0.0, "fees": 0.0, "net": 0.0, "count": 0, "margin": 0.0},
                "platforms": {}
            }

    try:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Item Title"]
            cleaned_title = title.strip().lower()
            
            if cleaned_title.startswith("m1"):
                platform = row["Platform"]
                gross_price = float(row["Sale Price"])
                
                try:
                    calculator = FeeCalculatorFactory.get_calculator(platform)
                    fees = calculator.calculate_fees(gross_price)
                    
                    commission = fees["commission"]
                    transaction_fee = fees["transaction_fee"]
                    flat_fee = fees["flat_fee"]
                    total_fees = fees["total_fees"]
                    net_payout = round(gross_price - total_fees, 2)
                    
                    # Store transaction record
                    matched_items.append({
                        "item_title": title,
                        "platform": platform.strip().title(),
                        "gross_price": gross_price,
                        "commission": commission,
                        "transaction_fee": transaction_fee,
                        "flat_fee": flat_fee,
                        "total_fees": total_fees,
                        "net_payout": net_payout
                    })
                    
                    # Accumulate globals
                    aggregate_gross += gross_price
                    aggregate_fees += total_fees
                    aggregate_net += net_payout
                    
                    # Accumulate platform breakdown
                    plt_name = platform.strip().title()
                    if plt_name not in platform_breakdown:
                        platform_breakdown[plt_name] = {
                            "gross": 0.0,
                            "fees": 0.0,
                            "net": 0.0,
                            "count": 0
                        }
                    platform_breakdown[plt_name]["gross"] += gross_price
                    platform_breakdown[plt_name]["fees"] += total_fees
                    platform_breakdown[plt_name]["net"] += net_payout
                    platform_breakdown[plt_name]["count"] += 1
                    
                except ValueError:
                    # Gracefully skip unsupported platforms
                    pass
    finally:
        if is_path:
            file.close()

    cumulative_margin_pct = (aggregate_net / aggregate_gross * 100) if aggregate_gross > 0 else 0.0
    
    return {
        "items": matched_items,
        "totals": {
            "gross": round(aggregate_gross, 2),
            "fees": round(aggregate_fees, 2),
            "net": round(aggregate_net, 2),
            "count": len(matched_items),
            "margin": round(cumulative_margin_pct, 2)
        },
        "platforms": platform_breakdown
    }


def run_parser():
    """
    Main function to run the CLI parser and print results.
    """
    # Get the directory where this script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to the CSV file relative to this script's directory.
    csv_path = os.path.join(script_dir, "mock_sales.csv")

    print(f"Reading sales data from: {csv_path}\n")
    print("--- Scanning for items starting with 'M1' & Calculating Multi-Platform Payouts ---\n")

    results = load_and_parse_sales(csv_path)

    # Print transaction details
    for item in results["items"]:
        print(f"Match Found! Item: '{item['item_title']}'")
        print(f"  Platform:     {item['platform']}")
        print(f"  Gross Price:  ${item['gross_price']:.2f}")
        print(f"  Fees Charged: ${item['total_fees']:.2f} (Commission: ${item['commission']:.2f} | Tx Fee: ${item['transaction_fee']:.2f} | Flat Fee: ${item['flat_fee']:.2f})")
        print(f"  Net Payout:   ${item['net_payout']:.2f}\n")

    # Print Dashboard
    print("=====================================================================")
    print("                   CONSIGNFLOW FINANCIAL DASHBOARD                   ")
    print("=====================================================================")
    print(f"Total Matches Processed: {results['totals']['count']}")
    print(f"Total Gross Revenue:     ${results['totals']['gross']:.2f}")
    print(f"Total Fees Deducted:     ${results['totals']['fees']:.2f}")
    print(f"Net Take-Home Revenue:   ${results['totals']['net']:.2f}")
    print(f"Cumulative Profit Margin: {results['totals']['margin']:.2f}%")
    print("---------------------------------------------------------------------")
    print("                         PLATFORM BREAKDOWN                          ")
    print("---------------------------------------------------------------------")
    print(f"{'Platform':<18} | {'Volume':<6} | {'Gross Sales':<11} | {'Total Fees':<10} | {'Efficiency':<10}")
    print("-" * 69)

    for plt_name, stats in results["platforms"].items():
        plt_gross = stats["gross"]
        plt_fees = stats["fees"]
        plt_net = stats["net"]
        plt_count = stats["count"]
        plt_efficiency = (plt_net / plt_gross * 100) if plt_gross > 0 else 0.0
        print(f"{plt_name:<18} | {plt_count:<6} | ${plt_gross:<10.2f} | ${plt_fees:<9.2f} | {plt_efficiency:.2f}%")

    print("=====================================================================\n")


if __name__ == "__main__":
    run_parser()
