import os
from dotenv import load_dotenv 
import pyreadstat
from pathlib import Path 

load_dotenv()

def get_finscope_path(year):
    """
    Constructs the path to FinScope data for a specific year,
    using a relative path structure that works across different computers
    with the same SharePoint sync structure.
    
    Args:
        year (int): The year of the FinScope data (e.g., 2003, 2004, etc.)
        
    Returns:
        Path: Path object pointing to the Stata data file
    """
    # Get the base path for FinScope data from the environment variable
    base_path = Path(os.getenv("DATA_PATH"))
    if not base_path:
        raise ValueError("DATA_PATH environment variable is not set.")

    # Construct the file path for the specific year
    file_path = base_path / "finscope" / "dta" / f"FS_{year}.dta"
    
    return file_path

def load_finscope_data(year):
    """
    Loads FinScope data for a specific year using pyreadstat to extract metadata.
    
    Args:
        year (int): The year of the FinScope data (e.g., 2003, 2004, etc.)
        
    Returns:
        tuple:  (DataFrame, metadata) where DataFrame contains the data and 
                metadata is a pyreadstat metadata object with variable labels,
                value labels, etc.
        
    Raises:
        FileNotFoundError: If the data file for the specified year doesn't exist
    """
    file_path = get_finscope_path(year)
    
    if not file_path.exists():
        raise FileNotFoundError(f"FinScope data file for {year} not found at: {file_path}")
    
    try:
        # Load the Stata file with pyreadstat to get both data and metadata
        data, metadata = pyreadstat.read_dta(str(file_path))
        print(f"Successfully loaded FinScope {year} data: {len(data)} rows")
        
        return data, metadata
    except Exception as e:
        print(f"Error loading FinScope {year} data: {str(e)}")
        raise


def load_finscope_sav(year):
    """
    Loads FinScope data for a specific year from a .sav (SPSS) file using pyreadstat.

    Args:
        year (int): The year of the FinScope data (e.g., 2003, 2004, etc.)

    Returns:
        tuple: (DataFrame, metadata) where DataFrame contains the data and
               metadata is a pyreadstat metadata object with variable labels,
               value labels, etc.

    Raises:
        FileNotFoundError: If the .sav data file for the specified year doesn't exist
    """
    base_path = Path(os.getenv("DATA_PATH"))
    if not base_path:
        raise ValueError("DATA_PATH environment variable is not set.")

    file_path = base_path / "finscope" / "sav" / f"FS_{year}.sav"

    if not file_path.exists():
        raise FileNotFoundError(f"FinScope .sav data file for {year} not found at: {file_path}")

    try:
        data, metadata = pyreadstat.read_sav(str(file_path))
        print(f"Successfully loaded FinScope {year} .sav data: {len(data)} rows")
        return data, metadata
    except Exception as e:
        print(f"Error loading FinScope {year} .sav data: {str(e)}")
        raise
