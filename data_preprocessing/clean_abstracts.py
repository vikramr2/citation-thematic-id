import pandas as pd

# Load the data
dois = pd.read_csv("../data/dois_with_crossref_metadata.csv")

# Remove the word "Abstract" from the abstracts
dois["abstract"] = dois["abstract"].str.replace("Abstract\n", "")

# Remove <p> and </p> tags from the abstracts, and <span> tags
dois["abstract"] = dois["abstract"].str.replace("<p>", "").str.replace("</p>", "").str.replace("<span>", "").str.replace("</span>", "")

# Save the cleaned data
dois.to_csv("../data/dois_with_abstracts.csv", index=False)