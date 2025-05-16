from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://application.axisbank.co.in/webforms/ApprovedProjectList/homeloans_request.aspx")  # Replace with your actual URL

# Create CSV file
csv_file = open('city_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
headers_written = False

# Function to get fresh dropdown element
def get_city_dropdown():
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlCity")))

# Get dropdown and options
city_dropdown = get_city_dropdown()
select = Select(city_dropdown)

# Iterate over cities
for i in range(1, len(select.options)):  # Skip first option if it's a placeholder
    try:
        # Re-locate dropdown and options to avoid stale elements
        city_dropdown = get_city_dropdown()
        select = Select(city_dropdown)
        options = select.options  # Refresh options list
        city_name = options[i].text  # Get fresh city name
        
        print(f"Processing city: {city_name}")

        # Select city and wait for table to load
        select.select_by_index(i)
        time.sleep(2)

        def process_current_page():
            global headers_written
            
            # Wait for table presence
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gvApprovedList")))
            rows = table.find_elements(By.TAG_NAME, "tr")

            if not headers_written:
                headers = [cell.text for cell in rows[0].find_elements(By.TAG_NAME, "th")]
                csv_writer.writerow(headers)
                headers_written = True

            # Extract data
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    csv_writer.writerow([city_name] + [cell.text for cell in cells])

        # Process first page
        process_current_page()

        # Handle pagination
        page_number = 2
        while True:
            pagination_links = driver.find_elements(By.CSS_SELECTOR, "#gvApprovedList a[href*='Page']")
            next_page_link = None

            for link in pagination_links:
                if f'Page${page_number}' in link.get_attribute('href'):
                    next_page_link = link
                    break

            if not next_page_link:
                break

            # Click next page
            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(2)  # Allow new page load

            # Process next page
            process_current_page()
            page_number += 1

    except Exception as e:
        print(f"Error processing city {city_name}: {e}")
        continue

# Cleanup
csv_file.close()
driver.quit()
