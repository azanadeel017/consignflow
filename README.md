# ConsignFlow

A multi-platform Business Intelligence (BI) engine and data pipeline built to parse bulk e-commerce ledgers, calculate platform-specific fee matrices, and output executive financial analytics.

---

## 📊 The Problem & The Solution

### The Business Bottleneck
High-volume sellers on live-stream and social commerce marketplaces (like Whatnot and TikTok Shop) manage hundreds of micro-transactions daily. Optimizing profit margins is incredibly difficult because channels use wildly different, multi-layered fee structures (varying percentage commissions, transaction processing rates, and flat per-item fees). Without automated data consolidation, tracking true channel efficiency is nearly impossible.

### The Engineering Architecture
`consignflow` bridges the gap between raw ledger data and operational strategy. Built in Python, the system parses incoming multi-platform CSV tables, filters targeted inventory batches (such as product lines prefixed with `M1`), and dynamically routes transactions through an enterprise-grade backend. 

Instead of an unstable chain of conditional statements, the engine leverages the **Strategy Design Pattern** paired with a **Simple Factory Pattern** to dynamically instantiate decoupled financial logic engines for each marketplace on the fly. 

The execution terminates by aggregating raw transactional data into a centralized **Financial Analytics Dashboard** that reveals macro-level profitability metrics and individual channel margin efficiencies.

---

## 🛠️ Software Design & Implementation

* **Architectural Design Patterns:** Implements an Object-Oriented `FeeCalculator` Strategy interface. New marketplaces can be integrated or updated independently without risking code regression or altering core data streaming lines.
* **Input Sanitization Pipeline:** Normalizes inconsistent raw ledger inputs by stripping whitespace anomalies and flattening text casing to guarantee matching precision across human-entered fields.
* **Centralized Business Intelligence:** Aggregates running data to calculate multi-channel KPIs:

$$\text{Cumulative Margin \%} = \left( \frac{\text{Total Net Revenue}}{\text{Total Gross Revenue}} \right) \times 100$$

$$\text{Channel Efficiency \%} = \left( \frac{\text{Channel Net Sales}}{\text{Channel Gross Sales}} \right) \times 100$$

---

## 📂 Project Structure

* `parser.py` — The core software pipeline executing the Strategy and Factory design patterns alongside the BI aggregation engine.
* `mock_sales.csv` — A multi-platform transaction ledger mapping diverse market channels.
* `ARCHITECTURE.md` — Technical system design notes outlining the UML class structure and OOP choices.
* `TODO.md` — Active development roadmap showing future scalability plans.

---

## 🚀 Live Analytics Console Output

Executing the pipeline via `uv run parser.py` yields high-fidelity ledger parsing followed by an automated operational dashboard:

```text
Reading sales data from: C:\...\mock_sales.csv
--- Scanning for items starting with 'M1' & Calculating Multi-Platform Payouts ---
Match Found! Item: 'M1 1996 Jordan Card'
  Platform:     Whatnot
  Gross Price:  $150.00
  Fees Charged: $16.65 (Commission: $12.00 | Tx Fee: $4.35 | Flat Fee: $0.30)
  Net Payout:   $133.35

Match Found! Item: 'M1 Vintage Nike Windbreaker'
  Platform:     TikTok Shop
  Gross Price:  $45.00
  Fees Charged: $3.00 (Commission: $2.70 | Tx Fee: $0.00 | Flat Fee: $0.30)
  Net Payout:   $42.00

=====================================================================
                   CONSIGNFLOW FINANCIAL DASHBOARD                   
=====================================================================
Total Matches Processed: 2
Total Gross Revenue:     $195.00
Total Fees Deducted:     $19.65
Net Take-Home Revenue:   $175.35
Cumulative Profit Margin: 89.92%
---------------------------------------------------------------------
                         PLATFORM BREAKDOWN                          
---------------------------------------------------------------------
Platform           | Volume | Gross Sales | Total Fees | Efficiency
---------------------------------------------------------------------
Whatnot            | 1      | $150.00     | $16.65     | 88.90%
Tiktok Shop        | 1      | $45.00      | $3.00      | 93.33%
=====================================================================
