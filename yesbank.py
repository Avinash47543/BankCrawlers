




# import time
# import csv
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# def scrape_yes_bank_projects():
#     # 🔧 Configure Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument('--disable-extensions')
#     chrome_options.add_argument('--disable-gpu')  # 🔧 Fix GPU/WebGL issue
#     chrome_options.add_argument('--enable-unsafe-webgl')
#     chrome_options.add_argument('--use-gl=desktop')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--ignore-certificate-errors')
#     chrome_options.add_argument('--disable-popup-blocking')
      
#     chrome_options.page_load_strategy = 'eager' 

#     # Initialize the webdriver with increased timeouts
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.set_page_load_timeout(300) 
#     driver.maximize_window()

#     try:
#         # Navigate to the Yes Bank approved projects page
#         url = "https://www.yesbank.in/approved-projects"
#         print(f"Navigating to {url}...")
#         driver.get(url)

#         # Wait for the page to load
#         wait = WebDriverWait(driver, 60)  # Increase wait time to 60 seconds

#         # Create a CSV file to store the results
#         csv_filename = "yes_bank_approved_projects.csv"

#         # Initialize CSV with headers
#         with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#             csv_writer = csv.writer(csvfile)
#             first_row = True  # Flag to write headers only once

#             #  Get all state options with retries
#             max_retries = 3
#             for attempt in range(max_retries):
#                 try:
#                     print(f"Waiting for state dropdown (attempt {attempt+1}/{max_retries})...")
#                     wait.until(EC.presence_of_element_located((By.ID, "state_drop")))
#                     state_dropdown = Select(driver.find_element(By.ID, "state_drop"))
#                     state_options = [option.text.strip() for option in state_dropdown.options if option.text.strip()]

#                     # Skip the first option if it's a placeholder like "Select State"
#                     if state_options and "Select" in state_options[0]:
#                         state_options = state_options[1:]

#                     print(f" Found {len(state_options)} states to process.")
#                     break
#                 except TimeoutException:
#                     if attempt < max_retries - 1:
#                         print(" Timeout waiting for state dropdown. Retrying...")
#                         driver.refresh()
#                         time.sleep(5)
#                     else:
#                         raise RuntimeError(" Failed to load state dropdown after multiple attempts.")

#             # 🌎 Loop through each state
#             for state in state_options:
#                 print(f" Processing state: {state}")

#                 # Select the state with retry
#                 for attempt in range(max_retries):
#                     try:
#                         state_dropdown = Select(driver.find_element(By.ID, "state_drop"))
#                         state_dropdown.select_by_visible_text(state)
#                         time.sleep(5)  # Wait for city dropdown to populate
#                         break
#                     except Exception as e:
#                         if attempt < max_retries - 1:
#                             print(f" Error selecting state {state}, retrying: {e}")
#                             time.sleep(3)
#                         else:
#                             print(f" Failed to select state {state}: {e}")
#                             continue

#                 # Get all city options for this state
#                 try:
#                     city_dropdown = Select(driver.find_element(By.ID, "city_drop"))
#                     city_options = [option.text.strip() for option in city_dropdown.options if option.text.strip()]

#                     # Skip the first option if it's a placeholder like "Select City"
#                     if city_options and "Select" in city_options[0]:
#                         city_options = city_options[1:]

#                     print(f" Found {len(city_options)} cities for {state}")

                    
#                     for city in city_options:
#                         print(f" Processing city: {city} in state: {state}")

#                         # Select the city with retry
#                         for attempt in range(max_retries):
#                             try:
#                                 city_dropdown = Select(driver.find_element(By.ID, "city_drop"))
#                                 city_dropdown.select_by_visible_text(city)
#                                 time.sleep(2)
#                                 break
#                             except Exception as e:
#                                 if attempt < max_retries - 1:
#                                     print(f" Error selecting city {city}, retrying: {e}")
#                                     time.sleep(3)
#                                 else:
#                                     print(f" Failed to select city {city}: {e}")
#                                     continue

#                         # Click the approve button with retry
#                         for attempt in range(max_retries):
#                             try:
#                                 approve_button = driver.find_element(By.ID, "approvebtn")
#                                 approve_button.click()
#                                 print(" Clicked approve button, waiting for results...")
#                                 break
#                             except Exception as e:
#                                 if attempt < max_retries - 1:
#                                     print(f" Error clicking approve button, retrying: {e}")
#                                     time.sleep(3)
#                                 else:
#                                     print(f" Failed to click approve button: {e}")
#                                     continue

#                         # Wait for the table to load
#                         try:
#                             wait.until(EC.presence_of_element_located((By.ID, "projectDataTable")))
#                             time.sleep(3)

#                             # Get the table
#                             table = driver.find_element(By.ID, "projectDataTable")

#                             # Extract headers if first row
#                             if first_row:
#                                 headers = table.find_elements(By.TAG_NAME, "th")
#                                 header_texts = [header.text.strip() for header in headers]
#                                 header_row = ["State", "City"] + header_texts  # Add state & city columns
#                                 csv_writer.writerow(header_row)
#                                 first_row = False
#                                 print(f" Headers: {header_row}")

#                             # Extract rows
#                             rows = table.find_elements(By.TAG_NAME, "tr")
#                             row_count = 0

#                             for row in rows[1:]:  # Skip header row
#                                 cells = row.find_elements(By.TAG_NAME, "td")
#                                 if cells:
#                                     row_data = [cell.text.strip() for cell in cells]
#                                     csv_writer.writerow([state, city] + row_data)
#                                     row_count += 1

#                             print(f" Scraped {row_count} projects for {city}, {state}")

#                         except TimeoutException:
#                             print(f" Timeout waiting for table for {city}, {state}")
#                         except Exception as e:
#                             print(f" Error processing table for {city}, {state}: {e}")

#                 except Exception as e:
#                     print(f"❌ Error processing cities for state {state}: {e}")
#                     continue

#         #  Save the CSV properly formatted
#         df = pd.read_csv(csv_filename)
#         print(f" Total records scraped: {len(df)}")
#         df.to_csv(csv_filename, index=False)

#     except Exception as e:
#         print(f" Critical error: {e}")

#     finally:
#         # Close the browser
#         print("🔚 Closing browser...")
#         driver.quit()
#         print(f" Scraping completed. Data saved to {csv_filename}")

# if __name__ == "__main__":
#     scrape_yes_bank_projects()

























import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_yes_bank_projects():
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')  
    chrome_options.add_argument('--disable-software-rasterizer')
      
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-popup-blocking')

    chrome_options.page_load_strategy = 'eager'  

    # Initialize the webdriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(120)  
    driver.maximize_window()

    try:
        url = "https://www.yesbank.in/approved-projects"
        print(f"Navigating to {url}...")
        driver.get(url)

        wait = WebDriverWait(driver, 60)  # Explicit wait

        csv_filename = "yes_bank_approved_projects.csv"

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            first_row = True  # Track header writing

            # Get all state options with retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"Waiting for state dropdown (attempt {attempt+1}/{max_retries})...")
                    wait.until(EC.presence_of_element_located((By.ID, "state_drop")))
                    state_dropdown = Select(driver.find_element(By.ID, "state_drop"))
                    state_options = [option.text.strip() for option in state_dropdown.options if option.text.strip()]

                    if state_options and "Select" in state_options[0]:
                        state_options = state_options[1:]

                    print(f"Found {len(state_options)} states to process.")
                    break
                except TimeoutException:
                    if attempt < max_retries - 1:
                        print("Timeout waiting for state dropdown. Retrying...")
                        driver.refresh()
                        time.sleep(5)
                    else:
                        raise RuntimeError("Failed to load state dropdown after multiple attempts.")

            # Loop through each state
            for state in state_options:
                print(f"Processing state: {state}")

                for attempt in range(max_retries):
                    try:
                        state_dropdown = Select(driver.find_element(By.ID, "state_drop"))
                        state_dropdown.select_by_visible_text(state)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "city_drop")))
                        break
                    except Exception as e:
                        if attempt < max_retries - 1:
                            print(f"Error selecting state {state}, retrying: {e}")
                            time.sleep(3)
                        else:
                            print(f"Failed to select state {state}: {e}")
                            continue

                # Get all city options
                try:
                    city_dropdown = Select(driver.find_element(By.ID, "city_drop"))
                    city_options = [option.text.strip() for option in city_dropdown.options if option.text.strip()]

                    if city_options and "Select" in city_options[0]:
                        city_options = city_options[1:]

                    print(f"Found {len(city_options)} cities for {state}")

                    for city in city_options:
                        print(f"Processing city: {city} in state: {state}")

                        for attempt in range(max_retries):
                            try:
                                city_dropdown = Select(driver.find_element(By.ID, "city_drop"))
                                city_dropdown.select_by_visible_text(city)
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "approvebtn")))
                                break
                            except Exception as e:
                                if attempt < max_retries - 1:
                                    print(f"Error selecting city {city}, retrying: {e}")
                                    time.sleep(3)
                                else:
                                    print(f"Failed to select city {city}: {e}")
                                    continue

                        for attempt in range(max_retries):
                            try:
                                approve_button = driver.find_element(By.ID, "approvebtn")
                                approve_button.click()
                                print("Clicked approve button, waiting for results...")
                                break
                            except Exception as e:
                                if attempt < max_retries - 1:
                                    print(f"Error clicking approve button, retrying: {e}")
                                    time.sleep(3)
                                else:
                                    print(f"Failed to click approve button: {e}")
                                    continue

                        try:
                            wait.until(EC.presence_of_element_located((By.ID, "projectDataTable")))
                            time.sleep(3)

                            table = driver.find_element(By.ID, "projectDataTable")

                            if first_row:
                                headers = table.find_elements(By.TAG_NAME, "th")
                                header_texts = [header.text.strip() for header in headers]
                                header_row = ["State", "City"] + header_texts
                                csv_writer.writerow(header_row)
                                first_row = False
                                print(f"Headers: {header_row}")

                            rows = table.find_elements(By.TAG_NAME, "tr")
                            row_count = 0

                            for row in rows[1:]:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if cells:
                                    row_data = [cell.text.strip() for cell in cells]
                                    csv_writer.writerow([state, city] + row_data)
                                    row_count += 1

                            print(f"Scraped {row_count} projects for {city}, {state}")

                        except TimeoutException:
                            print(f"Timeout waiting for table for {city}, {state}")
                        except Exception as e:
                            print(f"Error processing table for {city}, {state}: {e}")

                except Exception as e:
                    print(f"Error processing cities for state {state}: {e}")
                    continue

        # Save the CSV properly formatted
        df = pd.read_csv(csv_filename)
        print(f"Total records scraped: {len(df)}")
        df.to_csv(csv_filename, index=False)

    except Exception as e:
        print(f"Critical error: {e}")

    finally:
        print("Closing browser...")
        driver.quit()
        print(f"Scraping completed. Data saved to {csv_filename}")

if __name__ == "__main__":
    scrape_yes_bank_projects()
