import ollama
import chromadb
import pandas as pd
import argparse
import json

def get_doi_from_title(title, pubdata):
  return pubdata[pubdata["title"] == title]["doi"].values[0]

def find_title_in_paragraph(paragraph, titles):
    # Loop through each title in the array
    for title in titles:
        # Check if the title is present in the paragraph (case-insensitive search)
        if title.lower() in paragraph.lower():
            return title  # Return the title if found
    return None  # Return None if no title is found

def main():
  # Rewrite the above with argparse
  parser = argparse.ArgumentParser(description="Extract the thematic identity of a set of documents")
  parser.add_argument("--pubdata", type=str, help="Path to the CSV file containing the pubdata")
  parser.add_argument("--num_keywords", type=int, help="Number of keywords to extract")

  args = parser.parse_args()
  pubdata = pd.read_csv(args.pubdata)
  num_keywords = int(args.num_keywords)

  # Output dictionary
  output_dict = {}

  # Parse the titles and abstracts ito a list of strings in the format "Title: {title}, Abstract: {abstract}"
  documents = [f"Title: {title}, Abstract: {abstract}" for title, abstract in zip(pubdata["title"], pubdata["abstract"])]

  client = chromadb.Client()
  collection = client.create_collection(name="docs")

  # store each document in a vector embedding database
  for i, d in enumerate(documents):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
    embedding = response["embedding"]
    collection.add(
      ids=[str(i)],
      embeddings=[embedding],
      documents=[d]
  )
    
  # an example prompt
  prompt = f"List {num_keywords} specific detailed keywords that sum the overall thematic identity of these documents. Put brackets around the keywords. For example, [keyword1, keyword2, keyword3, etc]."

  # generate an embedding for the prompt and retrieve the most relevant doc
  response = ollama.embeddings(
    prompt=prompt,
    model="mxbai-embed-large"
  )
  results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=len(documents)
  )

  data = results['documents'][0]

  # generate a response combining the prompt and data we retrieved in step 2
  output = ollama.generate(
    model="llama2",
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
  )

  output_dict['keyword_explanation'] = output['response']

  # Parse the response into a list of keywords. Get the parts between the brackets, and split them by comma
  keywords = output['response'].split("[")[1].split("]")[0].split(", ")
  keywords = [keyword.lower() for keyword in keywords]
  output_dict['keywords'] = keywords

  # Further prompt the model to give the index of the document that best represents these keywords
  prompt = f'Which document best represents the keywords: {keywords}? Give the title as it appears in the dataset.'

  # generate a response combining the prompt and data we retrieved in step 2
  output2 = ollama.generate(
    model="llama2",
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
  )

  output_dict['thematic_center_explanation'] = output2['response']

  # Get the title of the document between the quotes
  title = find_title_in_paragraph(output2['response'], pubdata["title"])
  output_dict['thematic_center'] = title

  try:
    # Get the DOI of the document
    doi = get_doi_from_title(title, pubdata)
    output_dict['doi'] = doi
  except:
    output_dict['doi'] = "DOI not found"

  # Save the output to a JSON file
  with open("thematic_identity_output.json", "w") as f:
    json.dump(output_dict, f, indent=2)

if __name__ == "__main__":
  main()
