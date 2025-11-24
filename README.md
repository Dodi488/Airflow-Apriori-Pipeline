# Market Basket Analysis Pipeline (Airflow + Custom Apriori)

## 1. Project Title
**Data Mining Pipeline for Market Basket Analysis using Apache Airflow and Custom Apriori Algorithm**

---

## 2. Problem Description
This project implements an automated, daily data mining pipeline to discover **frequent itemsets** and **association rules** from simulated retail transaction data (Market Basket Analysis). The goal is to provide the data engineering team with a structured, reproducible system to identify items frequently bought together, which can inform business decisions such as product placement, promotional bundles, and inventory management.

---

## 3. Dataset Explanation (Transaction Simulation)
The pipeline is designed to process daily CSV files representing customer transactions.

* **Format:** Each row is a transaction, typically formatted as `TransactionID, Items` (e.g., `1, "Bread, Milk, Eggs"`).
* **Simulation:** The dataset is simulated using Python scripts to generate realistic market-basket data.
    * **Item Universe:** A small, fixed set of **5-20 unique items** (e.g., Bread, Milk, Beer, Chips, Eggs, etc.) is used to simplify the analysis and meet constraints.
    * **Generation Logic:** Transactions are generated with a probability bias to ensure certain items and itemsets appear together frequently, mimicking real-world purchasing patterns and guaranteeing interesting association rules are found (e.g., increasing the chance of `Milk` and `Bread` appearing together).
    * **Data Location:** Raw transaction files are stored in the `data/raw/` directory (e.g., `day1.csv`).

---

## 4. How to Run Airflow
This project assumes you have a local Apache Airflow environment set up.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Dodi488/Airflow-Apriori-Pipeline.git
    cd project/
    ```
2.  **Place DAG:** Ensure the `apriori_pipeline_dag.py` file is placed in your Airflow `dags/` folder.
3.  **Place Scripts/Data:** Ensure the supporting Python scripts (`scripts/` folder) and the sample data (`data/raw/`) are accessible to your Airflow workers/environment, following the required folder structure.
4.  **Start Airflow:** Start the Airflow Webserver and Scheduler (commands vary based on your setup, e.g., using Docker or a local environment).
5.  **Enable DAG:** Open the Airflow UI, find the `apriori_pipeline_dag`, and toggle it ON.
6.  **Trigger Run:** Manually trigger the DAG from the Airflow UI or wait for its scheduled run time.

---

## 5. DAG Description (Task by Task)
The Airflow DAG (**`apriori_pipeline_dag.py`**) orchestrates the data mining workflow, containing at least three sequential tasks.

| Task Name | Script File | Description |
| :--- | :--- | :--- |
| **`extract_clean_load_data`** | `scripts/load_data.py` / `scripts/clean_data.py` | 1. **Extract/Load:** Reads the raw CSV transaction file from `data/raw/`. 2. **Clean:** Splits the comma-separated item strings into lists and handles any potential nulls or duplicates. 3. **Output:** Saves the cleaned, processed transactions to `data/processed/cleaned_transactions.csv` (or JSON). |
| **`apriori_mining`** | `scripts/apriori.py` | 1. **Load:** Reads the cleaned transactions. 2. **Mine:** Executes the **custom Apriori implementation** to generate **frequent itemsets** (with Support) and **association rules** (with Support, Confidence, and Lift). |
| **`reporting_task`** | `scripts/generate_report.py` | 1. **Save Outputs:** Stores the calculated frequent itemsets and association rules as separate CSV files. 2. **Generate Report:** Creates a final summary report (Markdown/TXT/CSV) detailing the most frequent items, frequent pairs/triples, and top association rules. |

---

## 6. Explanation of Apriori Algorithm
The **Apriori Algorithm** is used to find frequent itemsets and generate association rules from transactional data.

### Your Version and Key Components
The custom implementation (`scripts/apriori.py`) adheres strictly to the requirement of **not using external data mining libraries** (like `mlxtend`).

1.  **Candidate Generation:** Iteratively generates candidate itemsets ($C_k$) of size $k$ from the frequent itemsets ($L_{k-1}$) of size $k-1$.
2.  **Pruning (Apriori Property):** This is the core efficiency step. It states that **if an itemset is frequent, then all of its subsets must also be frequent**. Candidates ($C_k$) whose $(k-1)$-size subsets are **not** in $L_{k-1}$ are immediately discarded without counting their support, drastically reducing computation.
3.  **Support Calculation:** The frequency of each candidate itemset in $C_k$ is counted against the total number of transactions to determine its **Support** (must exceed a minimum threshold, *Min_Support*).
4.  **Frequent Itemsets ($L_k$):** Candidates that meet the *Min_Support* threshold form the frequent itemsets $L_k$. This loop continues until no more frequent itemsets can be found.
5.  **Rule Generation:** Association rules of the form $X \rightarrow Y$ are generated from the final frequent itemsets $L_k$, where $X \cup Y = L_k$ and $X \cap Y = \emptyset$.

### Metrics for Rules

* **Support:** $P(X \cup Y)$. The proportion of transactions containing both $X$ and $Y$.
* **Confidence:** $P(Y|X)$. The probability that $Y$ is bought, given that $X$ is bought.
* **Lift:** $\frac{P(X \cup Y)}{P(X)P(Y)}$. Measures how much more likely $X$ and $Y$ are to be bought together than if they were independent. A value $>1$ suggests a positive association.

---

## 7. How to View Outputs
All generated outputs are stored in the **`project/results/`** directory.

* **Frequent Itemsets:** View the **`frequent_itemsets.csv`** file, which lists all itemsets meeting the *Min_Support* threshold and their corresponding support values.
* **Association Rules:** View the **`association_rules.csv`** file. This contains the Antecedent (X), Consequent (Y), and the computed Support, Confidence, and Lift for each rule.
* **Summary Report:** Check the **`summary_report.txt`** (or .md/.csv) for an easily readable summary of the top frequent items, frequent pairs, and the highest-confidence/lift rules.

---

## 8. Limitations & Improvements

### Limitations
* **Dataset Size:** The pipeline is constrained to small datasets (local execution only, no Big Data) and a maximum of 20 unique items. Performance on a large, real-world dataset would be slow due to the nature of the Apriori algorithm and lack of distributed computing.
* **Manual Apriori:** The requirement to implement Apriori manually means the code may not be as optimized as professional library versions.
* **Fixed Thresholds:** *Min_Support* and *Min_Confidence* thresholds are currently hardcoded; a dynamic approach would be better.

### Potential Improvements
* **External Data Source:** Migrate the Extract/Load task to pull data from a remote source (e.g., S3, Google Cloud Storage, or a database) instead of a local CSV file.
* **Dynamic Thresholds:** Add Airflow configuration parameters to allow *Min_Support* and *Min_Confidence* to be set dynamically at DAG run time.
* **Trend Analysis:** Add an optional task to compare today's discovered rules and itemset frequencies against historical results to identify emerging trends.
* **Visualization Task:** Add a dedicated task to generate and save charts (e.g., bar plots of top 10 itemset frequencies) to the `results/` folder.



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
