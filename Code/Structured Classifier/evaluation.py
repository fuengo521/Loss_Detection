import pandas as pd
import logging

logger = logging.getLogger(__name__)

def evaluate_model(df):
    # Evaluate model predictions against manual labels
    # Print out key metrics
    # Calculate match flags for 'new' and 'bulk'
    logger.info('evaluating model predictions')
    df['new_match'] = (df['new'] == df['NEW CONDITION']).astype(int)
    df['bulk_match'] = (df['bulk'] == df['BULK QUANTITY']).astype(int)
    
    logger.info("Number of items in test set: %s", len(df))
    logger.info("Number of items manually labeled as bulk: %s", df['BULK QUANTITY'].sum())
    logger.info("Number of items manually labeled as new: %s", df['NEW CONDITION'].sum())
    
    # Evaluate false positives/negatives
    false_positives = df[(df['bulk'] == 1) & (df['BULK QUANTITY'] == 0)]
    false_negatives = df[(df['bulk'] == 0) & (df['BULK QUANTITY'] == 1)]
    new_false_negatives = df[(df['new'] == 0) & (df['NEW CONDITION'] == 1)]
    new_false_positives = df[(df['new'] == 1) & (df['NEW CONDITION'] == 0)]
    
    both_misses = df[(df['bulk_match'] == 0) & (df['new_match'] == 0)]
    
    logger.info("Number of bulk false positives: %s", len(false_positives))
    logger.info("Number of bulk false negatives: %s", len(false_negatives))
    logger.info("Number of new false positives: %s", len(new_false_positives))
    logger.info("Number of new false negatives: %s", len(new_false_negatives))
    logger.info("Number of rows where both classifications were wrong: %s", len(both_misses))
    logger.info("Number of rows where both classifications were correct: %s", len(df[(df['new_match'] == 1) & (df['bulk_match'] == 1)]))
    
    logger.info("Rows where both classifications were wrong:")
    logger.info('\n%s', df[(df['new_match'] == 0) & (df['bulk_match'] == 0)].to_string())
