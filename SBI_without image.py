

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time

# # Setup Selenium WebDriver (Automatically downloads the required driver)
# options = webdriver.ChromeOptions()
#   # Run in headless mode
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

# # Initialize Chrome WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # Open the website
# url = "https://www.sbirealty.in/property-in-bhubaneshwar"
# driver.get(url)

# # Wait for the data to load
# time.sleep(5)  # Adjust if needed

# # Find the <ul> element with id "ulOtherCityProjects"
# try:
#     project_list = driver.find_element(By.ID, "ulOtherCityProjects")
#     project_items = project_list.find_elements(By.TAG_NAME, "li")  # Find all <li>

#     data = []

#     for li in project_items:
#         spans = li.find_elements(By.TAG_NAME, "span")

#         if len(spans) >= 6:
#             project_data = {
#                 "Builder Name": spans[0].text.strip(),
#                 "Project Name": spans[1].text.strip(),
#                 "City Name": spans[2].text.strip(),
#                 "Address 1": spans[3].text.strip(),
#                 "Address 2": spans[4].text.strip(),
#                 "No. of Units": spans[5].text.strip(),
#             }
#             data.append(project_data)

#     # Save data to CSV
#     df = pd.DataFrame(data)
#     csv_filename = "sbi_realty_projects_selenium.csv"
#     df.to_csv(csv_filename, index=False, encoding="utf-8")

#     print(f"✅ Data successfully saved to {csv_filename}")

# except Exception as e:
#     print("❌ Error:", str(e))

# # Close the browser
# driver.quit()





















from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.sbirealty.in/property-in-bhubaneshwar"
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ulOtherCityProjects")))

def scroll_and_wait():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_and_wait()

WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element((By.XPATH, "//ul[@id='ulOtherCityProjects']/li[1]"), "")
)

project_items = driver.find_elements(By.XPATH, "//ul[@id='ulOtherCityProjects']/li")

print(f"Found {len(project_items)} projects.")

data = []
for li in project_items:
    inner_html = li.get_attribute("innerHTML")
    spans = li.find_elements(By.TAG_NAME, "span")

    if len(spans) >= 6:
        project_data = {
            "Builder Name": spans[0].text.strip(),
            "Project Name": spans[1].text.strip(),
            "City Name": spans[2].text.strip(),
            "Address 1": spans[3].text.strip(),
            "Address 2": spans[4].text.strip(),
            "No. of Units": spans[5].text.strip(),
        }
        data.append(project_data)
    else:
        print(f"Skipping one entry. Content: {inner_html}")

if data:
    df = pd.DataFrame(data)
    csv_filename = "sbi_realty_projects.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"Data successfully saved to {csv_filename}")
else:
    print("No data extracted.")

driver.quit()
