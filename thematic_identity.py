import ollama
import chromadb
import pandas as pd
import argparse

def get_doi_from_title(title, pubdata):
  return pubdata[pubdata["title"] == title]["doi"].values[0]

def main():
  # Rewrite the above with argparse
  parser = argparse.ArgumentParser(description="Extract the thematic identity of a set of documents")
  parser.add_argument("--pubdata", type=str, help="Path to the CSV file containing the pubdata")
  parser.add_argument("--num_keywords", type=int, help="Number of keywords to extract")

  args = parser.parse_args()
  pubdata = pd.read_csv(args.pubdata)
  num_keywords = int(args.num_keywords)

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
  prompt = f"List {num_keywords} specific detailed keywords that sum the overall thematic identity of these documents. Answer in a single line with comma-separated format. Don't preface your answer with any words."

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

  # Parse the response into a list of keywords
  keywords = output['response'].replace('\n', '').split(", ")

  # Convert the list into lowercase
  keywords = [keyword.lower() for keyword in keywords]

  print()
  print(f'Thematic keywords: {keywords}')

  # Further prompt the model to give the index of the document that best represents these keywords
  prompt = f'Which document best represents the keywords: {keywords}? Just give me the title, no other text or prefacing, just the title only. No "Title: " prefix.'

  # generate a response combining the prompt and data we retrieved in step 2
  output2 = ollama.generate(
    model="llama2",
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
  )

  title = output2['response'].replace('\n', '').replace(".", "")
  print()
  print(f'Title: {title}')

  # Get the DOI of the document
  doi = get_doi_from_title(title, pubdata)
  print()
  print(f'DOI: {doi}')

if __name__ == "__main__":
  main()
