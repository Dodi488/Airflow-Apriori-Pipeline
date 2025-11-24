import json
import os
from itertools import combinations

# Configuration
MIN_SUPPORT = 0.2  # Item must appear in 20% of transactions
MIN_CONFIDENCE = 0.5 # Rule must be true 50% of the time

def get_frequent_itemsets(transactions, min_support):
    """
    Generates frequent itemsets using the Apriori strategy.
    """
    n_transactions = len(transactions)
    
    # Helper to calculate support for a specific candidate set
    def calculate_support(candidate_set):
        count = 0
        for t in transactions:
            if candidate_set.issubset(set(t)):
                count += 1
        return count / n_transactions

    # Phase 1: Frequent 1-itemsets
    item_counts = {}
    for t in transactions:
        for item in t:
            item_counts[item] = item_counts.get(item, 0) + 1
            
    frequent_itemsets = [] # Format: [{'items': ['A', 'B'], 'support': 0.5}]
    
    # Filter 1-itemsets
    l1 = []
    for item, count in item_counts.items():
        support = count / n_transactions
        if support >= min_support:
            l1.append(frozenset([item]))
            frequent_itemsets.append({'items': list([item]), 'support': support})
    
    current_l = l1
    k = 2

    # Phase 2: Iterate for k > 1
    while current_l:
        candidates = set()
        
        # Self-join to create candidates
        for i in range(len(current_l)):
            for j in range(i + 1, len(current_l)):
                union_set = current_l[i].union(current_l[j])
                if len(union_set) == k:
                    candidates.add(union_set)
        
        # Prune and Count Support
        next_l = []
        for candidate in candidates:
            support = calculate_support(candidate)
            if support >= min_support:
                next_l.append(candidate)
                frequent_itemsets.append({'items': list(candidate), 'support': support})
        
        current_l = next_l
        k += 1

    return frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence):
    """
    Generates association rules from frequent itemsets.
    Metric: Lift = Confidence / Support(Consequent)
    """
    rules = []
    
    # Map itemsets to their support for easy lookup
    support_map = {frozenset(entry['items']): entry['support'] for entry in frequent_itemsets}

    for entry in frequent_itemsets:
        itemset = frozenset(entry['items'])
        if len(itemset) < 2:
            continue
            
        support_itemset = entry['support']
        
        # Generate all non-empty subsets
        all_subsets = []
        for r in range(1, len(itemset)):
            all_subsets.extend(combinations(itemset, r))
            
        for subset in all_subsets:
            antecedent = frozenset(subset)
            consequent = itemset - antecedent
            
            support_antecedent = support_map.get(antecedent)
            
            # Confidence = Support(A U B) / Support(A)
            confidence = support_itemset / support_antecedent
            
            if confidence >= min_confidence:
                support_consequent = support_map.get(consequent)
                # Lift = Confidence / Support(B)
                lift = confidence / support_consequent
                
                rules.append({
                    'antecedent': list(antecedent),
                    'consequent': list(consequent),
                    'support': round(support_itemset, 4),
                    'confidence': round(confidence, 4),
                    'lift': round(lift, 4)
                })
    return rules

def run_mining():
    # Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_transactions.json')
    output_path = os.path.join(base_dir, 'data', 'processed', 'mining_results.json')

    print("Running Apriori Algorithm...")
    
    # Load Data
    with open(input_path, 'r') as f:
        transactions = json.load(f)

    # 1. Find Frequent Itemsets
    frequent_itemsets = get_frequent_itemsets(transactions, MIN_SUPPORT)
    print(f"Found {len(frequent_itemsets)} frequent itemsets.")

    # 2. Generate Rules
    rules = generate_rules(frequent_itemsets, MIN_CONFIDENCE)
    print(f"Generated {len(rules)} association rules.")

    # 3. Save Intermediate Results
    results = {
        "itemsets": frequent_itemsets,
        "rules": rules
    }
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved mining results to {output_path}")

if __name__ == "__main__":
    run_mining()
