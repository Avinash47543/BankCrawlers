
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://canarabank.com/housingprojects#")

wait = WebDriverWait(driver, 10)
time.sleep(3)  


dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "CityName"))))
cities = [option.text for option in dropdown.options if option.text.strip()]


with open("canaraBank_housing_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Sr.No.", "City/Place", "Project Name", "Builder Name"])
    
    for city in cities:
        dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "CityName"))))  # Re-locate dropdown
        dropdown.select_by_visible_text(city)
        time.sleep(2)  

    
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "BtnSubmit")))
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(3) 

       
        table = wait.until(EC.presence_of_element_located((By.ID, "tbllogdata")))
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skipping header row

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                record = [cols[i].text for i in range(4)]
                print(record)
                writer.writerow(record)  # Write to CSV in real-time
                f.flush()  # Ensure data is written immediately
                

# Close driver
driver.quit()
