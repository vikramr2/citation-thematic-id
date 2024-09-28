# citation-thematic-id
Use a prompt engineering approach with Ollama to get the thematic identity of a citation network cluster.

## Objectives

Given a citation network cluster, i.e. nodes (and their doi metadata) and edges (citations):
- Get the thematic identity of the cluster (what does this community study?)
- What is the most defining publication in this network thematically?

## Installation and Setup

1. Download Ollama [here](https://ollama.com/download)
2. Run `pip install ollama` in your Python environment
3. Pull the necessary models with the following command: `ollama pull llama2 mxbai-embed-large`
4. Clone this repository

## Running

First prep a csv with a `title` and `abstract` column. Just like [this](https://github.com/vikramr2/citation-thematic-id/blob/main/data/dois_with_abstracts.csv).

Then, run the following command from the root of the project:

```
python3 thematic_identity.py --pubdata {pubdata file} --num_keywords {integer value}
```
