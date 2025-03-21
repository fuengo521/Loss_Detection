import pandas as pd

def evaluate_model(df):
    # Evaluate model predictions against manual labels
    # Print out key metrics
    # Calculate match flags for 'new' and 'bulk'
    df['new_match'] = (df['new'] == df['NEW CONDITION']).astype(int)
    df['bulk_match'] = (df['bulk'] == df['BULK QUANTITY']).astype(int)
    
    print("Number of items in test set:", len(df))
    print("Number of items manually labeled as bulk:", df['BULK QUANTITY'].sum())
    print("Number of items manually labeled as new:", df['NEW CONDITION'].sum())
    
    # Evaluate false positives/negatives
    false_positives = df[(df['bulk'] == 1) & (df['BULK QUANTITY'] == 0)]
    false_negatives = df[(df['bulk'] == 0) & (df['BULK QUANTITY'] == 1)]
    new_false_negatives = df[(df['new'] == 0) & (df['NEW CONDITION'] == 1)]
    new_false_positives = df[(df['new'] == 1) & (df['NEW CONDITION'] == 0)]
    
    both_misses = df[(df['bulk_match'] == 0) & (df['new_match'] == 0)]
    
    print("Number of bulk false positives:", len(false_positives))
    print("Number of bulk false negatives:", len(false_negatives))
    print("Number of new false positives:", len(new_false_positives))
    print("Number of new false negatives:", len(new_false_negatives))
    print("Number of rows where both classifications were wrong:", len(both_misses))
    print("Number of rows where both classifications were correct:", len(df[(df['new_match'] == 1) & (df['bulk_match'] == 1)]))
    
    print("Rows where both classifications were wrong:")
    print(df[(df['new_match'] == 0) & (df['bulk_match'] == 0)])
