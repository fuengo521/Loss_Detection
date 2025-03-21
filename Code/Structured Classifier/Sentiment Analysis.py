from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load SBERT model and initialize labels
new_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
bulk_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

bulk_labels = {
    "1": "Plural items or large quantities of the same item, and"
}


new_labels = {
    "1": "Unopened, unused, new, sealed, or in original packaging."
}

new_texts = list(new_labels.values())
new_embeddings = new_model.encode(new_texts, normalize_embeddings=True)
bulk_texts = list(bulk_labels.values())
bulk_embeddings = bulk_model.encode(bulk_texts, normalize_embeddings=True)

def classify_sentiments_batch(phrases, model, sentiment_embeddings, sentiment_labels, batch_size=1000, threshold=0.5):

    results = []
    label_keys = list(sentiment_labels.keys())
    
    for i in range(0, len(phrases), batch_size):
        batch = phrases[i:i+batch_size]
        batch_embeddings = model.encode(batch, normalize_embeddings=True)

        similarities = util.cos_sim(batch_embeddings, sentiment_embeddings)
        
        for sim in similarities:
            best_match_idx = sim.argmax().item()
            best_match_score = sim[best_match_idx].item()
            
            if best_match_score < threshold:
                results.append("uncertain")
            else:
                results.append(label_keys[best_match_idx])
                
    return results

#Load data
#df = pd.read_csv('Craigslist_test.csv')
df = pd.read_csv(os.getenv('DATA_FILE'))
df = df.drop(columns=['origin_city', 'posted_time', 'cat_code','price', 'post_id', 'posted_location', 'scraped_time', 'post_link', 'category', 'LOW PRICE'])
df.head()
phrases = [title.lower().strip() for title in df['title'].tolist()]

# Classify sentiments in batches with the threshold
df['new'] = classify_sentiments_batch(phrases, new_model, new_embeddings, new_labels, batch_size=100, threshold=0.3)
df['bulk'] = classify_sentiments_batch(phrases, bulk_model, bulk_embeddings, bulk_labels, batch_size=100, threshold=0.12)
df['bulk'] = df['bulk'].replace({'1': 1, "uncertain": 0})
df['new'] = df['new'].replace({'1': 1, "uncertain": 0})
df.head(100)
print("Number of items in test set:", len(df))
print("Number of items manually labeled as bulk:", df['BULK QUANTITY'].sum())
print("Number of items manually labeled as new:", df['NEW CONDITION'].sum())

#Calcualate accuracy compared to manual labels
df['new_match'] = ((df['new'] == df['NEW CONDITION'])).astype(int)
df['bulk_match'] = ((df['bulk'] == df['BULK QUANTITY'])).astype(int)
df['bulk_match'].sum()
df['new_match'].sum()

15/23
bulk_misses = df[df['bulk_match'] == 0]
new_misses = df[df['new_match'] == 0]
(df[df['bulk_match']==0])
both_misses = df[(df['bulk_match'] == 0) & (df['new_match'] == 0)]
both_misses
false_positives = df[(df['bulk'] == 1) & (df['BULK QUANTITY'] == 0)]
print("Number of bulk false positives:", len(false_positives))
false_negatives = df[(df['bulk'] == 0) & (df['BULK QUANTITY'] == 1)]
print("Number of bulk false negatives:", len(false_negatives))


new_false_negatives = df[(df['new'] == 0) & (df['NEW CONDITION'] == 1)]
len(new_false_negatives)
new_false_positives = df[(df['new'] == 1) & (df['NEW CONDITION'] == 0)]
print("Number of new false positives:", len(new_false_positives))
print("Number of new false negatives:", len(new_false_negatives))
print("Number of rows where both classifications were wrong:", len(both_misses))
print("Number of rows where both classifications were correct:", len(df[(df['new_match'] == 1) & (df['bulk_match'] == 1)]))

#Rows where both classifications were wrong
print("Rows where both classifications were wrong:")
print(df[(df['new_match'] == 0) & (df['bulk_match'] == 0)])

print("*****************Now moving onto retailer analysis*****************")
#List of retailers for retailer analysis
stores = [
    "7-Eleven", "ACME", "aerie", "Ahold Delhaize", "Albertsons", "ALLEN EDMONDS", "alo", "amazon", "AMERICAN EAGLE", "AMOCO",
    "ampm", "Apple", "ARC'TERYX", "at home", "AT&T", "Athleta", "AutoZone", "Banana Republic", "Bass Pro Shops", "Bath & Body Works",
    "Belle Tire", "BEST BUY", "BIG LOTS!", "BJ'S", "Blain's Farm & Fleet", "bloomingdales", "Bob's Discount Furniture", "BOOT BARN", "bp", "Brookfield Properties",
    "Bubba’s 33", "Bunnings Warehouse", "Cabela’s", "Caleres", "Callaway", "CarQuest Auto Parts", "Chestnut Market", "Circle K", "Columbia", "Cracker Barrel Old Country Store",
    "CVS Health", "Denny’s", "DICK’S", "Dollar General", "Dollar Tree", "Domino’s", "DSW Designer Shoe Warehouse", "Duane Reade", "EssilorLuxottica", "EXCHANGE",
    "Family Dollar", "Famous Footwear", "Food Lion", "Forever 21", "Gabe's", "Gap", "Giant", "Golf Galaxy", "Gucci", "Guess",
    "Hannaford", "Harbor Freight", "Harris Teeter", "Helzberg Diamonds", "Hershey", "Hibbett | City Gear", "H&M", "Home Chef", "HomeGoods", "Home Sense",
    "IKEA", "Jack Wolfskin", "Jaggers", "Jared", "JCPenney", "Jewel Osco", "Kay Jewelers", "Keke's Breakfast Cafe", "King Soopers", "Kohl's",
    "Kroger", "LEGO", "LensCrafters", "Loblaw Companies Limited", "Lowe's", "Lululemon", "Macy's", "Mall of America", "Market Basket (by Price Chopper)", "Marshalls",
    "Mattress Firm", "Meijer", "Michaels", "Mountain Hardwear", "Murphy USA", "Naturalizer", "Next (NEX / MCX)", "Nike", "Nordstrom", "Northeast Grocery",
    "O'Reilly Auto Parts", "Odyssey", "Office Depot", "OfficeMax", "Ogio", "Old Navy", "Parkers Kitchen", "Party City", "Phillips Edison & Company", "PINK",
    "Planet Fitness", "prAna", "Price Chopper", "Public Lands", "Publix", "RALPH LAUREN", "Ralphs", "REI Co-op", "Retail Business Services", "Rexall",
    "Rite Aid", "ROSS Dress for Less", "Safeway", "Sam's Club", "Schnucks", "Shaws", "Signet Jewelers", "Smith's", "Sorel", "Speedway",
    "Sportsman's Warehouse", "Staples", "Stine", "Stripes", "Sunglass Hut", "Target", "Texas Roadhouse", "The Home Depot", "The ODP Corporation", "The RealReal",
    "The Shoe Company", "Thorntons", "TJX", "T.J.Maxx", "Topgolf", "Topgolf Callaway Brands", "Tops Friendly Markets", "Tractor Supply Co.", "TravelCenters of America", "Truist Financial",
    "Ulta Beauty", "Verizon", "VS&Co", "Vons", "Vuori", "Walgreens", "Walmart", "Wawa", "Wayfair", "Wegmans",
    "Weis", "Wesfarmers", "Whole Foods Market", "Winners"
]

#Sample data for this one, test set had no instances
data = pd.DataFrame({
    'title': [
        "Walmart medications in bulk",
        "7-Eleven snacks and drinks",
        "Home Depot lot of hammers",
        "No store here",
        "10 Apple Iphones",
        'JBL Speaker',
        "asafreppovahjergn",
        'Stapls school supplies',
    ]
})
data.head()

# Remove special characters and extra whitespace, convert to lowercase

def normalize_text(text):
    if pd.isna(text):
        return None
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[^\w\s]', '', text.lower().strip())
    return ' '.join(text.split())

# Preprocess the stores list
stores_normalized = [normalize_text(s) for s in stores]

# Function to find the best matching retailer name
def find_best_match(text, choices, threshold=70):
    if pd.isna(text) or not isinstance(text, str):
        return None
    
    text_normalized = normalize_text(text)
    
    match = process.extractOne(text_normalized, choices, scorer=fuzz.token_set_ratio)
    
    if match and match[1] >= threshold:
        original_store = [s for s in stores if normalize_text(s) == match[0]][0]
        return original_store
    return None

#With Example data
data['matched_store'] = data['title'].apply(lambda x: find_best_match(x, stores_normalized))

#Display the results
print('Sample Data results:')
print(data[['title', 'matched_store']])

#Misses mispellings still...("Stapls" on row 7)

#Show scores
print("\nDebugging Similarity Scores:")
for title in data['title']:
    if pd.notna(title):
        matches = process.extract(normalize_text(title), stores_normalized, scorer=fuzz.token_set_ratio, limit=3)
        print(f"Title: '{title}' -> Top Matches: {matches}")


print("Num retailers in training set:", df['RETAILER NAME'].sum())

#Apply to test set to show
df['retailer'] = df['title'].apply(lambda x: find_best_match(x, stores_normalized))
print(df[['title', 'retailer']])

#print all rows where retailer is not None
filtered_data = df[df['retailer'].notna()]
filtered_data.head()

#Find sus ratings from this
df['number_retailer'] = df['retailer'].notna().astype(int)
df['og_sus']= df['NEW CONDITION']   + df['BULK QUANTITY']+ df['RETAILER NAME']
df['new_sus'] = df['new'] + df['bulk'] + df['number_retailer']
df['og_sus'].sum()
df['new_sus'].sum()
df['error'] = ((df['og_sus'] - df['new_sus'])**2)**.5
wrong_sus = df[df['error'] > 0]
len(wrong_sus)


#False sus and not detected sus
false_sus = df[(df['og_sus'] == 0) & (df['new_sus'] != 0)]
false_sus.head(len(false_sus))
not_detected_sus = df[(df['og_sus'] != 0) & (df['new_sus'] == 0)]
not_detected_sus.head(len(not_detected_sus))
print("Number of initially sus rows not detected:", len(not_detected_sus))
print("Number of false sus rows detected:", len(false_sus))
sus = df[(df['og_sus'] != 0)]
print("Number of rows that are sus:", len(sus))


len(false_sus)+len(not_detected_sus)