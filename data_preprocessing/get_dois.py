import pandas as pd
from sys import argv

EDGELIST_FILE = argv[1]
METADATA_FILE = argv[2]

edgelist = pd.read_csv(EDGELIST_FILE)

# Get the DOIs for the citing and cited nodes
metadata = pd.read_csv(METADATA_FILE)
metadata = metadata[['id', 'doi']]

# Only keep the rows where the id is in the edgelist
metadata = metadata[metadata['id'].isin(edgelist['citing']) | metadata['id'].isin(edgelist['cited'])]

metadata.to_csv('dois.csv', index=False)
