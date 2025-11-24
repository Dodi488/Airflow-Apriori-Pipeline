import pandas as pd
import os

def load_and_clean_data():
    # 1. Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'raw', 'day1.csv')
    output_dir = os.path.join(base_dir, 'data', 'processed')
    output_path = os.path.join(output_dir, 'cleaned_transactions.json')

    print(f"Reading from: {input_path}")

    # 2. Load Data
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # 3. Clean Data
    # List comprehension to split strings and strip whitespace
    transactions = [
        [item.strip() for item in row.split(',')] 
        for row in df.iloc[:, 1]
    ]

    # 4. Save using Pandas
    # Wrap the list in a Series to use the .to_json() method
    os.makedirs(output_dir, exist_ok=True)
    
    # orient='values' ensures we get a simple list of lists: [["A"], ["B"]]
    # instead of an indexed dictionary: {"0": ["A"], "1": ["B"]}
    pd.Series(transactions).to_json(output_path, orient='values')

    print(f"Successfully saved {len(transactions)} transactions to {output_path}")

if __name__ == "__main__":
    load_and_clean_data()
