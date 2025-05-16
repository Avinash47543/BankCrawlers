import pandas as pd
import re

# Load CSV safely
try:
    df = pd.read_csv("testing.csv", dtype=str, on_bad_lines="skip")  # Read all as strings
except Exception as e:
    print("Error reading CSV:", e)
    exit()

# Remove rows that have more than 4 columns
df = df.dropna(axis=1, how="all")  # Remove completely empty columns (if any)
df = df[df.columns[:4]]  # Keep only the first 4 columns

# Function to check if a city name is invalid (contains numbers, dots, or special characters)
def is_invalid_city(city):
    return bool(re.search(r'[^A-Za-z\s]', str(city)))  # Allows only letters and spaces

# Filter out invalid city names (assuming City Name is in the **first column**)
df_filtered = df[~df.iloc[:, 0].apply(is_invalid_city)]  

# Save cleaned data
df_filtered.to_csv("cleaned_testing.csv", index=False)
print("✅ Cleaned CSV saved as 'cleaned_testing.csv'")

