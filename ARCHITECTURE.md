# ConsignFlow System Architecture

This document outlines how the data filtering engine functions.

## Data Pipeline Flowchart

[mock_sales.csv] ---> (parser.py Engine) ---> Filters for 'M1' ---> [Console Output]

## Core Logic
1. The script dynamically locates `mock_sales.csv` using absolute system pathing.
2. It streams rows using Python's built-in `csv.DictReader` to conserve memory.
3. It runs a case-insensitive string check (`.strip().lower()`) to filter out target items.