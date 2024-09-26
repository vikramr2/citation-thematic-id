import pandas as pd
from sys import argv

INPUT_FILE = argv[1]
EDGELIST_FILE = argv[2]
CLUSTER_ID = int(argv[3])

df = pd.read_csv(INPUT_FILE, sep='\t', header=None)
edgelist = pd.read_csv(EDGELIST_FILE, sep='\t', header=None)

# Filter out the cluster with the given ID
df = df[df[1] == CLUSTER_ID]

nodes = df[0].tolist() 

# Get the edgelist for the cluster
edgelist = edgelist[edgelist[0].isin(nodes) & edgelist[1].isin(nodes)]

# Name thwe columns citing and cited
edgelist.columns = ['citing', 'cited']

edgelist.to_csv(f'cluster_{CLUSTER_ID}_edgelist.csv', index=False)
