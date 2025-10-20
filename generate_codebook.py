import os
import pandas as pd
import pyreadstat
from dotenv import load_dotenv
from pathlib import Path 
from utils import get_finscope_path, load_finscope_data

# Create the codebook folder if it doesn't exist
codebook_folder = Path("codebook")
codebook_folder.mkdir(exist_ok=True)

# Loop through years 2005 to 2019 to load data and create codebooks
for year in range(2005, 2020):
    try:
        df, metadata = load_finscope_data(year)
        
        # Create a DataFrame for the codebook
        df_m = pd.DataFrame()
        df_m['name'] = metadata.column_names
        df_m['label'] = metadata.column_labels
        
        # Save the codebook as a CSV file
        codebook_path = codebook_folder / f"codebook_{year}.csv"
        df_m.to_csv(codebook_path, index=False)
        print(f"Codebook for {year} saved to {codebook_path}")
    except Exception as e:
        print(f"Failed to process data for {year}: {e}")

