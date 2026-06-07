# ApexPlanet Data Analytics Internship - Task 1

## Project Overview
This repository contains the deliverables for **Task 1: Data Immersion & Wrangling** as part of the 60-day Data Analytics Internship at ApexPlanet Software Pvt. Ltd. The primary objective of this task is to profile, clean, and transform an unstructured, corrupted transactional dataset into an analysis-ready format.

---

## Data Dictionary
The dataset contains transaction-level sales data. Below is the documentation of the schema rules and business relevance applied during the data immersion phase:

| Column Name | Data Type | Description | Potential Business Relevance |
| :--- | :--- | :--- | :--- |
| **Order_ID** | String / Object | Unique alphanumeric identifier for each sales transaction (Format: `ORDXXXXX`). | Tracks unique sales records, order volumes, and serves as the primary key for auditing single transactions. |
| **Order_Date** | Datetime | The standardized date on which the transaction was placed (`YYYY-MM-DD`). | Crucial for time-series analysis, identifying seasonality patterns, monthly revenue growth, and sales trends. |
| **Customer_ID**| String / Object | Unique alphanumeric identifier for the customer placing the order (Format: `CUSTXXXX`). | Used for customer retention analysis, purchase frequency tracking, and loyalty segmentation. |
| **Quantity** | Integer | Total units of items purchased within the specific order. | Vital for inventory management, supply chain demand forecasting, and bulk purchase tracking. |
| **Unit_Price** | Float | The price per single unit of the product sold. | Helps evaluate pricing strategies, competitive tiering, and profit margin estimations. |
| **Total_Price**| Float | Total monetary value of the transaction ($Quantity \times Unit\_Price$). | Core financial performance metric used to calculate total revenue and isolate high-value orders. |

---

## Data Quality Issues Identified & Fixed
During the initial data profiling stage, several critical pipeline blockers were discovered and resolved via the automated cleaning script:
1. **Structural Concatenation**: Cleaned instances where text fields were mashed directly into dates without spaces (e.g., `ORD100002025-02-25` or `2025-12-31CUST3952`).
2. **Inconsistent Delimiters**: Standardized date fields utilizing erratic characters like `.`, `-`, `:`, or whitespaces.
3. **Missing Structural Values**: Dropped records completely missing primary keys (`Order_ID`) and imputed incomplete `Total_Price` values mathematically where structural components existed.