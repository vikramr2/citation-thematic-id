import pandas as pd
from sys import argv

INPUT_FILE = argv[1]
SIZE_THRESHOLD = int(argv[2])

df = pd.read_csv(INPUT_FILE)

# Filter out clusters with less than SIZE_THRESHOLD members
df = df[df['n'] >= SIZE_THRESHOLD]

df.to_csv(INPUT_FILE, index=False)
