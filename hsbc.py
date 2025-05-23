
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize WebDriver
service = Service('chromedriver.exe')  
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.hsbc.co.in/home-loans/list-of-projects/')

# Wait for links to load
wait = WebDriverWait(driver, 10)
city_links = driver.find_elements(By.CSS_SELECTOR, "a.A-LNKC28L-RW-ALL")

# Extract city names and URLs
city_data = [(link.text.strip(), link.get_attribute("href")) for link in city_links]

data_list = []  # Store data

for city_name, city_url in city_data:
    driver.get(city_url) 
    time.sleep(3) 
    
    try:
        
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            th = row.find_elements(By.TAG_NAME, "th")  # Project name is in <th>
            tds = row.find_elements(By.TAG_NAME, "td")  # Builder & Area are in <td>
            
            if th and len(tds) >= 2: 
                project_name = th[0].text.strip()
                builder_name = tds[0].text.strip()
                area = tds[1].text.strip()
                
                
                data_list.append([city_name, project_name, builder_name, area])
    
    except Exception as e:
        print(f"Error processing {city_url}: {e}")
    
    driver.back()
    time.sleep(2)  # Wait before processing the next city

driver.quit()


columns = ['City', 'Project name', 'Builder name', 'Area']
df = pd.DataFrame(data_list, columns=columns)


df['City'].fillna(method='ffill', inplace=True)

df.to_csv('hsbc_home_loans.csv', index=False)

print("Scraping completed and data saved to hsbc_home_loans.csv")
