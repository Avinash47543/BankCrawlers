
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


driver = webdriver.Chrome()
url = "https://www.indusind.com/in/en/personal/loans/home-loan/approved-project-list.html"
driver.get(url)


table = driver.find_element(By.XPATH, "//table")


header_row = table.find_elements(By.TAG_NAME, "th")
headers = [th.text.strip() for th in header_row]


rows = table.find_elements(By.TAG_NAME, "tr")
data = []
for row in rows[1:]:  # Skip the header row
    cells = row.find_elements(By.TAG_NAME, "td")
    data.append([cell.text.strip() for cell in cells])

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)  # Add headers


df.to_csv("IndusIndproject_list.csv", index=False)


driver.quit()

print("Table with headers extracted and saved as 'approved_project_list.csv'.")
