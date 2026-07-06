# ConsignFlow

A Python tool that automates scanning through bulk e-commerce sales sheets to calculate exact take-home profits after platform fees.

---

## The Motivation

Selling in volume on live-stream marketplaces like Whatnot creates a massive data headache. When you are dealing with hundreds of quick micro-transactions, calculating your actual profit margins manually is incredibly tedious. Platforms don't just take a simple flat rate; they layer commissions, processing percentages, and flat per-item fees on top of each other. 

I built `consignflow` to eliminate this bottleneck. The script automatically parses raw CSV sales ledgers, filters out specific inventory batches (like product lines starting with the prefix `M1`), and pushes the numbers through a precise fee matrix. Instead of digging through spreadsheets, a seller gets a clean console breakdown of their exact net payout instantly.

---

## How It Works Under the Hood

Instead of overcomplicating the stack, I focused on making the script fast and resilient against bad data:

* **File Management:** Uses Python’s native `os` and `csv` modules to cleanly map file paths and stream data tables without needing heavy external libraries.
* **Input Sanitization:** Cleans up messy data inputs automatically. The script trims accidental trailing spaces and flattens text casing (e.g., converting " M1 " or "m1" perfectly) so human typing errors in the inventory log don't break the system.
* **The Math Logic:** Tracks the exact live fee breakdown used by major resale platforms:

$$\text{Commission} = \text{Gross Price} \times 0.08$$

$$\text{Processing Fee} = (\text{Gross Price} \times 0.029) + 0.30$$

$$\text{Net Payout} = \text{Gross Price} - (\text{Commission} + \text{Processing Fee})$$

---

## Project Structure

* `parser.py` — The core logic, string parsing routines, and financial math.
* `mock_sales.csv` — A simulated multi-platform ledger used to test the code.
* `ARCHITECTURE.md` — Notes on system design and why I chose this specific layout.
* `TODO.md` — My active feature roadmap for future updates to the engine.

---

## Example Console Output

Running the script via `uv run parser.py` prints out a clear, line-by-line financial breakdown for matching items:

```text
Reading sales data from: C:\...\mock_sales.csv
--- Scanning for items starting with 'M1' & Calculating Payouts ---

Match Found! Item: 'M1 Vintage Tee'
  Gross Price:  $50.00
  Whatnot Fees: $5.75 (8% Commission: $4.00 | 2.9% Tx Fee: $1.45 | Flat Fee: $0.30)
  Net Payout:   $44.25

Total matching items found: 1
