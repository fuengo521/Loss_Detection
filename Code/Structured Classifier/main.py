from data_loader import load_data
from models import new_model, bulk_model, new_labels, bulk_labels, new_embeddings, bulk_embeddings, classify_sentiments_batch
from retailer import normalize_text, find_best_match
from evaluation import evaluate_model
import pandas as pd
import logging
from logger_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def main():
    # Load and preprocess data
    logger.info('starting main execution')
    df = load_data()
    
    # Prepare list of listing titles (lowercase, stripped)
    phrases = [title.lower().strip() for title in df['title'].tolist()]
    
    # Run sentiment classification for 'new' and 'bulk'
    logger.info("running sentiment classification for 'new'")
    df['new'] = classify_sentiments_batch(phrases, new_model, new_embeddings, new_labels, batch_size=100, threshold=0.3)
    logger.info("running sentiment classification for 'bulk'")
    df['bulk'] = classify_sentiments_batch(phrases, bulk_model, bulk_embeddings, bulk_labels, batch_size=100, threshold=0.12)
    
    # Replace predictions: '1' becomes 1 and 'uncertain' becomes 0
    df['bulk'] = df['bulk'].replace({'1': 1, "uncertain": 0})
    df['new'] = df['new'].replace({'1': 1, "uncertain": 0})
    
    # Evaluate model predictions against manual labels
    logger.info('evaluating model performance')
    evaluate_model(df)
    
    # Retailer analysis
    logger.info('starting retailer analysis')
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
        "Ulta Beauty", "Verizon", "VS&Co", "Vons", "Vuori", "Walgreens", "Wawa", "Wayfair", "Wegmans",
        "Weis", "Wesfarmers", "Whole Foods Market", "Winners"
    ]
    
    # Normalize retailer names for matching
    stores_normalized = [normalize_text(s) for s in stores]
    df['retailer'] = df['title'].apply(lambda x: find_best_match(x, stores_normalized, threshold=70, original_choices=stores))
    logger.info('retailer matching complete')
    print(df[['title', 'retailer']])
    
    # Compute a basic "sus" score as per current logic (to be improved later)
    df['number_retailer'] = df['retailer'].notna().astype(int)
    df['og_sus'] = df['NEW CONDITION'] + df['BULK QUANTITY'] + df['RETAILER NAME']
    df['new_sus'] = df['new'] + df['bulk'] + df['number_retailer']
    df['error'] = ((df['og_sus'] - df['new_sus'])**2)**0.5
    wrong_sus = df[df['error'] > 0]
    logger.info("Number of rows where sus score differs: %s", len(wrong_sus))
    
if __name__ == "__main__":
    main()
