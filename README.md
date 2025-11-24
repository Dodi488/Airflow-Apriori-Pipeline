# Airflow Apriori Pipeline: Bookstore Edition

**Tech Stack:** Python, Apache Airflow, Pandas 

## 1. Project Overview
This project implements a complete data mining pipeline orchestrated with **Apache Airflow**. It simulates a daily market-basket analysis for a small bookstore. The system ingests raw transaction data, cleans it, and runs a custom implementation of the **Apriori algorithm** (built from scratch without external mining libraries) to discover frequent itemsets and association rules.

## 2. Problem Description
The scenario involves a small retail startup (a bookstore) that receives a daily CSV file containing customer purchases. The business needs to automate the analysis of these transactions to understand buying patterns, specifically:
* **Frequent Itemsets:** Which books/items are often bought together?
* **Association Rules:** If a customer buys *Harry Potter 1*, are they likely to buy *Harry Potter 2*?

The pipeline automates the ingestion, processing, mining, and reporting of these insights.

## 3. Dataset
The project uses simulated transaction data.
* **Format:** CSV (`TransactionID, Items`)
* **Content:** Each row represents a single transaction containing a list of items separated by commas.
* **Item Universe:** A small set (approx. 10 items) including titles like *1984, Animal Farm, Harry Potter* and accessories like *Bookmarks* and *Tote Bags*.

## 4. Project Structure
The repository follows a modular structure as required:

```text
project/
├── dags/
│   └── apriori_pipeline_dag.py
├── data/
│   ├── raw/
│   │   └── day1.csv
│   ├── processed/
│   │   └── cleaned_transaction.py
│   └── results/
│       ├── frequent_itemset.csv
│       └── association_rules.csv
├── models/
├── scripts/
│   ├── load_data.py
│   ├── clean_data.py
│   ├── apriori.py
│   └── generate_report.py
└── README.md
