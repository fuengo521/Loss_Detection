import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv() # Loads environment variables

def load_data():
    # Loads and preprocesses CSV data
    # Drops unnecessary cols
    data_file = os.getenv('DATA_FILE')
    df = pd.read_csv(data_file)
    
    df = df.drop(columns=[
        'origin_city',
        'posted_time',
        'cat_code',
        'price',
        'post_id',
        'posted_location',
        'scraped_time',
        'post_link',
        'category',
        'LOW PRICE'
        ])
    
    return df