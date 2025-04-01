#GET API KEY FROM GOOGLE CLOUD PLATFORM
#https://aistudio.google.com/apikey
#INSERT KEY INTO API_KEYS Array

import pandas as pd
import time
import google.generativeai as genai
import os

API_KEYS = []


# Batch sizes for each model per run (UNUSED IN CURRENT ROTATION LOGIC)
MODEL_BATCH_SIZES = {
    "gemini-2.0-flash-lite": 30,
    "gemini-2.0-flash": 15,
    "gemini-2.0-flash-thinking": 10, # Ensure this key matches others
    "gemini-1.5-flash": 15
}

# Minimum time between requests for each model (in seconds)
# IMPORTANT: Verify these delays meet actual API RPM limits
MODEL_RATE_LIMITS = {
    "gemini-2.0-flash-lite": 2,
    "gemini-2.0-flash": 6,
    "gemini-2.0-flash-thinking": 6, # Key must be consistent
    "gemini-1.5-flash": 6
}

# Daily request limits for each model per API Key
# IMPORTANT: Verify these match your account quotas
DAILY_REQUEST_LIMITS = {
    "gemini-2.0-flash-lite": 1500,
    "gemini-2.0-flash": 1500,
    "gemini-2.0-flash-thinking": 1500, # Key must be consistent
    "gemini-1.5-flash": 1500
}

# --- Original Model Generation Functions ---
# IMPORTANT: Verify the actual model ID strings inside these functions are correct!

def generate_text_gemini_2_flash(api_key, prompt):
    model_id_internal = 'models/gemini-2.0-flash' # Verify this ID
    short_name = "gemini-2.0-flash" # For error message
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id_internal)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"!! API Error ({short_name}, Key ...{api_key[-4:]}): {e}")
        return None

def generate_text_gemini_2_flash_lite(api_key, prompt):
    model_id_internal = 'models/gemini-2.0-flash-lite' # Verify this ID
    short_name = "gemini-2.0-flash-lite" # For error message
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id_internal)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"!! API Error ({short_name}, Key ...{api_key[-4:]}): {e}")
        return None

def generate_text_gemini_2_flash_thinking(api_key, prompt):
    # CRITICAL: Ensure this is the correct, valid model ID you intend to use
    model_id_internal = 'models/gemini-2.0-flash-thinking-exp-01-21'
    short_name = "gemini-2.0-flash-thinking" # For error message
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id_internal)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"!! API Error ({short_name}, Key ...{api_key[-4:]}): {e}")
        return None

def generate_text_gemini_15_flash(api_key, prompt):
    model_id_internal = 'models/gemini-1.5-flash' # Verify this ID
    short_name = "gemini-1.5-flash" # For error message
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id_internal)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"!! API Error ({short_name}, Key ...{api_key[-4:]}): {e}")
        return None

# Function dictionary for easy lookup (using short names)
model_functions = {
    "gemini-2.0-flash-lite": generate_text_gemini_2_flash_lite,
    "gemini-2.0-flash": generate_text_gemini_2_flash,
    "gemini-2.0-flash-thinking": generate_text_gemini_2_flash_thinking,
    "gemini-1.5-flash": generate_text_gemini_15_flash
}

# Validate that all models have necessary configurations
MODEL_SHORT_NAMES = list(model_functions.keys())
for name in MODEL_SHORT_NAMES:
    if name not in MODEL_RATE_LIMITS:
        raise ValueError(f"Rate limit not defined for model: {name}")
    if name not in DAILY_REQUEST_LIMITS:
        raise ValueError(f"Daily limit not defined for model: {name}")
    # MODEL_BATCH_SIZES check omitted as it's unused in this logic

# --- Input/Output Files ---
INPUT_CSV = "Craigslist_test_10k.csv"
OUTPUT_CSV = "Craigslist_10k_output.csv"

# === Prompt Definition === (Unchanged)
def set_prompt(str1, str2, str3, str4, str5):
    prompt = f'''
    Analyze the following listing data and assign a likelihood score (1-100) indicating the probability that the item is stolen. Use the following criteria:
    Company Name Mentioned:
    If the title contains a retailer name (e.g., "Home Depot", "CVS", "Walgreens"), increase the score.
    New Condition Keywords:
    If the title includes words like "new", "unused", "unopened", "with tag", "fresh", "unaltered", "never", "untried", "nib", increase the score.
    Bulk Quantity Keywords:
    If the title includes words like "bulk", "lot", "reseller", "a lot of", increase the score.
    Significantly Lower Price:
    If the listed price is much lower than typical retail value, increase the score. This is a strong indicator of stolen goods.
    Scaling:
    A listing with no suspicious keywords should have a score close to 1.
    A listing that meets all criteria should have a score close to 100.
    Partial matches should be scaled accordingly.

    Process the following listing data and return only the numbers in a single line, separated by commas:
    Listing 1: {str1}
    Listing 2: {str2}
    Listing 3: {str3}
    Listing 4: {str4}
    Listing 5: {str5}

    Output only a list of CSV-formatted numbers in the order of the 5 listings (e.g., 10,75,30,5,90). Do not include any other text or explanation.
    '''
    return prompt


# === Processing Logic (with Strict Rotation) ===

def process_data():
    # --- Initialization ---
    print("Loading data...")
    try:
        df = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_CSV}' not found.")
        return
    print(f"Loaded {len(df)} rows from {INPUT_CSV}")

    if "likelihood_score" not in df.columns:
        df["likelihood_score"] = pd.NA

    output_file_exists = os.path.exists(OUTPUT_CSV)
    processed_rows = 0
    start_row_index = 0 # Index in the original df to start processing from

    if output_file_exists:
        try:
            # Attempt to count processed rows (simple line count)
            with open(OUTPUT_CSV, "r") as f:
                 lines = f.readlines()
                 # Basic check if header might exist
                 has_header = len(lines) > 0 and "title" in lines[0].lower() # Adjust if needed
                 processed_rows = len(lines) - 1 if has_header else len(lines)
                 processed_rows = max(0, processed_rows) # Ensure not negative

            if processed_rows > 0 and processed_rows < len(df):
                 start_row_index = processed_rows
                 print(f"Output file '{OUTPUT_CSV}' found. Resuming from row {start_row_index + 1} (approx based on line count).")
            elif processed_rows >= len(df):
                 print("All rows appear processed based on output file length.")
                 return
            else: # processed_rows == 0
                 print("Starting processing from beginning.")
                 output_file_exists = False # Treat as new file for header writing
        except Exception as e:
            print(f"Warning: Could not accurately determine processed rows from {OUTPUT_CSV}: {e}. Processing all rows.")
            output_file_exists = False # Treat as new file

    df_unprocessed = df.iloc[start_row_index:]
    total_rows_to_process = len(df_unprocessed)

    if total_rows_to_process == 0 and processed_rows < len(df):
         print("Warning: Resume logic resulted in zero rows to process, but output file has fewer rows than input. Check resume logic or output file.")
         return
    elif total_rows_to_process == 0:
        print("No rows to process.")
        return

    # --- State Variables ---
    num_api_keys = len(API_KEYS)
    ordered_model_list = MODEL_SHORT_NAMES # Use the short names for rotation order
    num_models = len(ordered_model_list)

    current_api_key_index = 0 # Start with the first key
    current_model_index = 0   # Start with the first model in rotation

    last_request_time = {model_name: 0 for model_name in ordered_model_list}

    daily_usage = {}
    for key_index in range(num_api_keys):
        daily_usage[key_index] = {model_name: 0 for model_name in ordered_model_list}

    def model_reached_daily_limit(model_name, key_index):
        # Check if model_name exists in the limits before accessing
        if model_name not in DAILY_REQUEST_LIMITS:
             print(f"Warning: Daily limit definition missing for model '{model_name}'. Assuming not limited.")
             return False
        # Check if the key_index and model_name exist in usage tracker
        if key_index not in daily_usage or model_name not in daily_usage[key_index]:
             print(f"Warning: Daily usage tracking missing for model '{model_name}' on key index {key_index}. Assuming not limited.")
             return False # Or handle error differently
        return daily_usage[key_index][model_name] >= DAILY_REQUEST_LIMITS[model_name]


    batch_size = 5

    print(f"\nStarting processing loop for {total_rows_to_process} rows with {num_models} models and {num_api_keys} API keys.")
    print(f"Model rotation order: {ordered_model_list}")

    # --- Main Batch Loop ---
    # Iterate using the index of the unprocessed dataframe
    for batch_start_index in range(0, total_rows_to_process, batch_size):
        
        # Global check if all keys exhausted
        all_keys_fully_exhausted = True
        for k_idx in range(num_api_keys):
             if not all(model_reached_daily_limit(m_name, k_idx) for m_name in ordered_model_list):
                   all_keys_fully_exhausted = False
                   break
        if all_keys_fully_exhausted:
            print("STOP: All API keys have reached their daily limits for all models.")
            break

        # Prepare batch data using iloc on the unprocessed slice
        batch_df = df_unprocessed.iloc[batch_start_index:min(batch_start_index + batch_size, total_rows_to_process)]
        if batch_df.empty:
            continue

        padded_batch = batch_df.copy()
        if len(padded_batch) < batch_size:
             num_to_pad = batch_size - len(padded_batch)
             # Create padding rows with columns matching the main df
             padding_data = {col: ["Empty listing (padding)" if col == "title" else 0 if col == "price" else "None" if col == "category" else None] * num_to_pad
                            for col in df.columns if col != "likelihood_score"} # Exclude score column
             padding = pd.DataFrame(padding_data)
             padded_batch = pd.concat([padded_batch, padding], ignore_index=True)

        # Create prompt strings
        str1 = f"Title: {padded_batch.iloc[0].get('title', '')}, Price: ${padded_batch.iloc[0].get('price', 0)}, Category: {padded_batch.iloc[0].get('category', '')}"
        str2 = f"Title: {padded_batch.iloc[1].get('title', '')}, Price: ${padded_batch.iloc[1].get('price', 0)}, Category: {padded_batch.iloc[1].get('category', '')}"
        str3 = f"Title: {padded_batch.iloc[2].get('title', '')}, Price: ${padded_batch.iloc[2].get('price', 0)}, Category: {padded_batch.iloc[2].get('category', '')}"
        str4 = f"Title: {padded_batch.iloc[3].get('title', '')}, Price: ${padded_batch.iloc[3].get('price', 0)}, Category: {padded_batch.iloc[3].get('category', '')}"
        str5 = f"Title: {padded_batch.iloc[4].get('title', '')}, Price: ${padded_batch.iloc[4].get('price', 0)}, Category: {padded_batch.iloc[4].get('category', '')}"
        prompt = set_prompt(str1, str2, str3, str4, str5)

        # --- Model/Key Selection and Attempt Loop ---
        processed_successfully = False
        models_attempted_this_batch = 0
        primary_api_key_index_for_batch = current_api_key_index
        attempt_api_key_index = primary_api_key_index_for_batch

        while not processed_successfully and models_attempted_this_batch < num_models:

            model_name = ordered_model_list[current_model_index] # Get SHORT name
            api_key = API_KEYS[attempt_api_key_index]
            key_idx_for_msg = attempt_api_key_index + 1

            print(f"-- Batch {batch_start_index//batch_size + 1}/{ (total_rows_to_process + batch_size - 1)//batch_size }: Attempting Model '{model_name}' (Rot. Index {current_model_index}) with Key {key_idx_for_msg} --")

            if model_reached_daily_limit(model_name, attempt_api_key_index):
                print(f"-> Daily limit reached for '{model_name}' on Key {key_idx_for_msg}.")
                found_alternative_key = False
                for next_key_offset in range(1, num_api_keys):
                    next_key_idx = (attempt_api_key_index + next_key_offset) % num_api_keys
                    if not model_reached_daily_limit(model_name, next_key_idx):
                         print(f"--> Switching to Key {next_key_idx + 1} for this attempt.")
                         attempt_api_key_index = next_key_idx
                         found_alternative_key = True
                         break
                if found_alternative_key:
                    continue

                print(f"-> All API keys checked/exhausted for '{model_name}'. Skipping model.")
                current_model_index = (current_model_index + 1) % num_models
                models_attempted_this_batch += 1
                attempt_api_key_index = primary_api_key_index_for_batch # Reset key
                continue

            # Rate Limit Check
            current_time = time.time()
            time_since_last_request = current_time - last_request_time.get(model_name, 0)
            # Use .get for rate limit in case a model was missing from the dict (though checked earlier)
            rate_limit_delay = MODEL_RATE_LIMITS.get(model_name, 1) # Default to 1s if missing
            required_wait = rate_limit_delay - time_since_last_request

            if required_wait > 0:
                print(f"-> Waiting {required_wait:.2f}s for rate limit on '{model_name}'...")
                time.sleep(required_wait)

            # API Call
            api_key = API_KEYS[attempt_api_key_index] # Ensure correct key
            print(f"-> Calling model '{model_name}' with Key {attempt_api_key_index + 1}...")
            generate_function = model_functions[model_name] # Get function using short name
            generated_text = generate_function(api_key, prompt) # Call specific function
            last_request_time[model_name] = time.time()

            # Process Response
            if generated_text:
                try:
                    num_list = [int(num.strip()) for num in generated_text.split(",")]
                    actual_batch_indices = batch_df.index # Use index of the original slice

                    if len(num_list) >= len(actual_batch_indices):
                        scores_to_assign = num_list[:len(actual_batch_indices)]
                        df.loc[actual_batch_indices, "likelihood_score"] = scores_to_assign

                        output_batch = df.loc[actual_batch_indices].copy()
                        # Recalculate header need based on whether the *first overall row* is being written
                        is_first_overall_row = actual_batch_indices[0] == df.index[0]
                        write_header = (not output_file_exists) and is_first_overall_row
                        output_batch.to_csv(OUTPUT_CSV, mode="a", header=write_header, index=False)
                        output_file_exists = True # Prevent header rewrite

                        daily_usage[attempt_api_key_index][model_name] += 1
                        print(f"-> OK! Batch processed. Usage for '{model_name}' on Key {attempt_api_key_index + 1}: {daily_usage[attempt_api_key_index][model_name]}/{DAILY_REQUEST_LIMITS.get(model_name, 'N/A')}")
                        processed_successfully = True

                    else: # Wrong number of scores
                        print(f"-> Parse Error: Expected {len(actual_batch_indices)} scores, got {len(num_list)}. Response: '{generated_text[:100]}...'")

                except ValueError: # Not integers
                     print(f"-> Parse Error: Could not convert response to integers. Response: '{generated_text[:100]}...'")
                except Exception as e: # Other parsing error
                     print(f"-> Parse Error: Unexpected error: {e}. Response: '{generated_text[:100]}...'")
            else: # API call failed
                 print(f"-> API call failed for '{model_name}' on Key {attempt_api_key_index + 1}.")

            # Post-Attempt Logic
            if processed_successfully:
                current_model_index = (current_model_index + 1) % num_models
                current_api_key_index = primary_api_key_index_for_batch # Reset primary key index
                break
            else:
                print(f"-> Attempt failed. Moving to next model.")
                current_model_index = (current_model_index + 1) % num_models
                models_attempted_this_batch += 1
                attempt_api_key_index = primary_api_key_index_for_batch # Reset key index

        # End of While Loop for batch attempts
        if not processed_successfully:
            print(f"!! Batch {batch_start_index//batch_size + 1} FAILED after trying all models/keys. Skipping.")
            current_model_index = (current_model_index + 1) % num_models # Ensure rotation for next batch
            current_api_key_index = primary_api_key_index_for_batch

    print("\nProcessing complete!")


# === Execution ===
if __name__ == "__main__":
    process_data()