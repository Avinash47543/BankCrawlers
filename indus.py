# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import pandas as pd

# # Initialize the WebDriver (Ensure you have the ChromeDriver installed)
# driver = webdriver.Chrome()

# # Open the webpage
# url = "https://www.indusind.com/in/en/personal/loans/home-loan/approved-project-list.html"
# driver.get(url)

# # Locate the table
# table = driver.find_element(By.XPATH, "//table")

# # Extract table rows
# rows = table.find_elements(By.TAG_NAME, "tr")

# # Store table data
# data = []
# for row in rows:
#     cells = row.find_elements(By.TAG_NAME, "td")  # Change to "th" for header row
#     data.append([cell.text.strip() for cell in cells])

# # Convert to DataFrame
# df = pd.DataFrame(data)

# # Save to CSV
# df.to_csv("approved_project_list.csv", index=False, header=False)

# # Close the browser
# driver.quit()

# print("Table extracted and saved as 'approved_project_list.csv'.")




























from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()
url = "https://www.indusind.com/in/en/personal/loans/home-loan/approved-project-list.html"
driver.get(url)

# Locate the table
table = driver.find_element(By.XPATH, "//table")

# Extract headers (th elements)
header_row = table.find_elements(By.TAG_NAME, "th")
headers = [th.text.strip() for th in header_row]

# Extract table rows (td elements)
rows = table.find_elements(By.TAG_NAME, "tr")
data = []
for row in rows[1:]:  # Skip the header row
    cells = row.find_elements(By.TAG_NAME, "td")
    data.append([cell.text.strip() for cell in cells])

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)  # Add headers

# Save to CSV
df.to_csv("IndusIndproject_list.csv", index=False)

# Close browser
driver.quit()

print("Table with headers extracted and saved as 'approved_project_list.csv'.")
