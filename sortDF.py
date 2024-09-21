import pandas as pd
import numpy as np
import json
movies = pd.read_csv("movies_cleaned.csv")
print(movies.head(),movies.columns)
print(movies['title'].isna().sum())
