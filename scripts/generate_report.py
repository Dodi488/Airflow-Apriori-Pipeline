import json
import pandas as pd
import os

def generate_csv_reports():
    # Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'processed', 'mining_results.json')
    results_dir = os.path.join(base_dir, 'data', 'results')
    
    os.makedirs(results_dir, exist_ok=True)

    print("Generating Reports...")

    # Load Mining Results
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Mining results not found. Run apriori.py first.")
        return

    # 1. Save Frequent Itemsets CSV
    # Flatten items list to string "A, B"
    itemsets_data = []
    for entry in data['itemsets']:
        itemsets_data.append({
            'itemset': ", ".join(entry['items']),
            'support': entry['support']
        })
    
    df_itemsets = pd.DataFrame(itemsets_data)
    # Sort by support descending
    df_itemsets = df_itemsets.sort_values(by='support', ascending=False)
    df_itemsets.to_csv(os.path.join(results_dir, 'frequent_itemsets.csv'), index=False)
    print("Saved frequent_itemsets.csv")

    # 2. Save Association Rules CSV
    rules_data = []
    for entry in data['rules']:
        rules_data.append({
            'antecedent': ", ".join(entry['antecedent']),
            'consequent': ", ".join(entry['consequent']),
            'support': entry['support'],
            'confidence': entry['confidence'],
            'lift': entry['lift']
        })

    df_rules = pd.DataFrame(rules_data)
    # Sort by Lift descending to show strongest rules first
    if not df_rules.empty:
        df_rules = df_rules.sort_values(by='lift', ascending=False)
    
    df_rules.to_csv(os.path.join(results_dir, 'association_rules.csv'), index=False)
    print("Saved association_rules.csv")

if __name__ == "__main__":
    generate_csv_reports()
