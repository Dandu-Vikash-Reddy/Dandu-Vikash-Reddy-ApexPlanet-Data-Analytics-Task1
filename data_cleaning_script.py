import pandas as pd
import numpy as np
import re
import os

def clean_apexplanet_dataset(input_path, output_path):
    """
    Reads a raw text-based extraction of the ApexPlanet dataset,
    profiles its quality issues, cleans structural anomalies using Regex,
    and outputs a pristine, analysis-ready CSV file.
    """
    print("=== [1/4] Initializing ApexPlanet Data Wrangling Engine ===")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Target file '{input_path}' not found.")
        return
        
    with open(input_path, 'r') as file:
        raw_lines = file.readlines()
        
    cleaned_rows = []
    
    # Optimized Regular Expressions to catch complex structural mashups
    order_pattern = re.compile(r'(ORD\d{5})')
    date_pattern = re.compile(r'(\d{4}[-./:\s]\d{2}[-./:\s]\d{2})')
    customer_pattern = re.compile(r'(CUST\d{4})')
    
    # Captures numeric fields at the tail end: Quantity, Unit Price, Total Price
    numeric_pattern = re.compile(r'(\d+)\s+([\d.]+)\s+([\d.]+)\s*$')

    print("=== [2/4] Parsing Unstructured Records via Regular Expressions ===")
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract patterns
        order_match = order_pattern.search(line)
        date_match = date_pattern.search(line)
        cust_match = customer_pattern.search(line)
        numeric_match = numeric_pattern.search(line)
        
        # Build clean values
        order_id = order_match.group(1) if order_match else np.nan
        
        # Standardize chaotic date delimiters into YYYY-MM-DD strings
        order_date = date_match.group(1) if date_match else np.nan
        if pd.notna(order_date):
            order_date = re.sub(r'[-./:\s]', '-', order_date)
            
        customer_id = cust_match.group(1) if cust_match else np.nan
        
        if numeric_match:
            quantity = int(numeric_match.group(1))
            unit_price = float(numeric_match.group(2))
            total_price = float(numeric_match.group(3))
        else:
            quantity, unit_price, total_price = np.nan, np.nan, np.nan
            
        cleaned_rows.append({
            "Order_ID": order_id,
            "Order_Date": order_date,
            "Customer_ID": customer_id,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Total_Price": total_price
        })

    # Create Primary Dataframe
    df = pd.DataFrame(cleaned_rows)
    
    print("\n=== [3/4] Running Comprehensive Data Quality Diagnostics ===")
    print(f"-> Total Processed Elements: {len(df)}")
    print("-> Missing Data Counts:")
    print(df.isnull().sum())
    
    # Drop rows containing completely empty primary identifiers
    df.dropna(subset=['Order_ID'], inplace=True)
    
    # Fill structural missing gaps safely
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Customer_ID'].fillna("UNKNOWN_CUSTOMER", inplace=True)
    
    # Feature Engineering Check: Re-calculate missing Total Prices mathematically
    missing_price_mask = df['Total_Price'].isnull() & df['Quantity'].notnull() & df['Unit_Price'].notnull()
    df.loc[missing_price_mask, 'Total_Price'] = df['Quantity'] * df['Unit_Price']
    
    # Remove duplicate order entries
    initial_count = len(df)
    df.drop_duplicates(subset=['Order_ID'], keep='first', inplace=True)
    print(f"-> Deduplication: Dropped {initial_count - len(df)} duplicate transactions.")
    
    print("\n=== [4/4] Transporting Cleaned Dataset to Target Dest ===")
    df.to_csv(output_path, index=False)
    print(f"-> Production File successfully saved to: '{output_path}'")

if __name__ == "__main__":
    clean_apexplanet_dataset("raw_dataset_extraction.txt", "Cleaned_Dataset_Task1.csv")