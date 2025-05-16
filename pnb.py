import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_pnb_housing():
    # Initialize the webdriver
    driver = webdriver.Chrome()  # You can use Firefox, Edge, etc.
    driver.maximize_window()
    
    # Open the target website
    url = "https://www.pnbindia.in/housing-projects.aspx"
    driver.get(url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    
    # Find the dropdown element
    dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_drpPlace"]')))
    select = Select(dropdown)
    
    # Get all options from dropdown
    options = select.options
    
    # Create CSV file and write headers
    with open('pnb.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Initialize headers flag
        headers_written = False
        
        # Loop through each dropdown option
        for i in range(1, len(options)):  # Start from 1 to skip the "Select" option
            # Select option by index
            select.select_by_index(i)
            
            # Click the search button
            search_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnsearch")
            search_button.click()
            
            # Wait for the table to load or refresh
            time.sleep(5)
            
            # Check if table exists
            table_exists = True
            try:
                table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            except:
                table_exists = False
                print(f"No table found for option: {options[i].text}")
                continue
                
            if table_exists:
                # Get table rows
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                # Skip if there are no rows
                if len(rows) <= 1:  # Only header row exists
                    print(f"No data found for option: {options[i].text}")
                    continue
                
                # Write headers if not already written
                if not headers_written:
                    header_cells = rows[0].find_elements(By.TAG_NAME, "th")
                    headers = [cell.text.strip() for cell in header_cells]
                    csv_writer.writerow(headers)
                    headers_written = True
                
                # Process data rows (skip header row)
                for row in rows[1:]:
                    # Check if row is expanded (has data)
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        csv_writer.writerow(row_data)
                        
            # Reset dropdown for next iteration
            select = Select(driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_drpPlace"]'))
    
    # Close the browser
    driver.quit()
    print("Scraping completed. Data saved to pnb.csv")

if __name__ == "__main__":
    scrape_pnb_housing()