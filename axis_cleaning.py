import pandas as pd
import re


try:
    df = pd.read_csv("testing.csv", dtype=str, on_bad_lines="skip")  
except Exception as e:
    print("Error reading CSV:", e)
    exit()


df = df.dropna(axis=1, how="all")  
df = df[df.columns[:4]]  


def is_invalid_city(city):
    return bool(re.search(r'[^A-Za-z\s]', str(city)))  
# Filter out invalid city names (assuming City Name is in the **first column**)
df_filtered = df[~df.iloc[:, 0].apply(is_invalid_city)]  

# Save cleaned data
df_filtered.to_csv("cleaned_testing.csv", index=False)
print("✅ Cleaned CSV saved as 'cleaned_testing.csv'")

