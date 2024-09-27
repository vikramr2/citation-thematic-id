import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

tqdm.pandas()

def clean_abstract(abstract):
    # Parse the abstract using BeautifulSoup to remove XML-like tags
    soup = BeautifulSoup(abstract, 'lxml')
    return soup.get_text()

def get_metadata_from_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        title = data["message"].get("title", ["Title not found"])[0]
        abstract = data["message"].get("abstract", "Abstract not found")
        
        # Clean the abstract to remove XML tags
        clean_abs = clean_abstract(abstract) if abstract != "Abstract not found" else abstract
        return title, clean_abs
    else:
        return None, None

# Load doi dataframes
dois = pd.read_csv("../data/dois.csv")

# Use pandas apply to get metadata for each DOI
dois["title"], dois["abstract"] = zip(*dois["doi"].progress_apply(get_metadata_from_doi))

# Save metadata to a new CSV file
dois.to_csv("../data/dois_with_crossref_metadata.csv", index=False)
