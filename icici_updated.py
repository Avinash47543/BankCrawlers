
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

url = "https://home.icicibank.com/home?ITM=nli_cms_hlbt_productnavigation_Approved-Projects"
driver.get(url)
wait = WebDriverWait(driver, 120)

def safe_get_text(el, selector):
    try:
        return el.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return "N/A"

otp_done = False

# Step 1: Open city dropdown
city_input = wait.until(EC.element_to_be_clickable((By.ID, "txtCity")))
city_input.click()
time.sleep(2)

# Step 2: Click "Show More" if present
try:
    show_more_btn = driver.find_element(By.CSS_SELECTOR, "a.s_more")
    if show_more_btn.get_attribute("data-show-more-status") == "hidded":
        driver.execute_script("arguments[0].click();", show_more_btn)
        time.sleep(2)  
except Exception as e:
    print("No 'Show More' button found or already expanded:", e)



# Step 3: Get updated city list
city_elements = driver.find_elements(By.CSS_SELECTOR, ".bropbox.drop_box li")
city_names = [el.text.strip() for el in city_elements if el.text.strip()]
print(f"Found {len(city_names)} cities.")
print("Cities:", city_names)

# Step 4: Prepare CSV
with open("icici_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Project Name", "Builder Name", "RERA No.", "Location", "City", "Bedroom", "Bank"])

    for city_index, city_name in enumerate(city_names):
        print(f"\nSearching for: {city_name}")

        try:
            # Reopen the dropdown every time
            city_input = wait.until(EC.element_to_be_clickable((By.ID, "txtCity")))
            city_input.click()
            time.sleep(1.5)

            try:
                show_more_btn = driver.find_element(By.CSS_SELECTOR, "a.s_more")
                if show_more_btn.get_attribute("data-show-more-status") == "hidded":
                    driver.execute_script("arguments[0].click();", show_more_btn)
                    time.sleep(2)
            except Exception as e:
                print("No 'Show More' button found or already expanded:", e)

            
            city_elements = driver.find_elements(By.CSS_SELECTOR, ".bropbox.drop_box li")
            matched = False
            for city_el in city_elements:
                city_text = city_el.text.strip().lower()
                if city_name.lower() in city_text:
                    ActionChains(driver).move_to_element(city_el).click().perform()
                    matched = True
                    break

            if not matched:
                print(f"Could not match city: {city_name}")
                continue

            # Click search
            search_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSearch_new")))
            search_btn.click()

            # Wait for OTP only once
            if not otp_done:
                print("Please complete mobile number and OTP verification manually.")
                input("Press ENTER after OTP verification is done and projects are visible...")
                otp_done = True

            # Scroll to load all projects
            prev_count = 0
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                cards = driver.find_elements(By.CSS_SELECTOR, ".project.approved.uc, .project.approved.r2m, .project.approvedundefined")
                curr_count = len(cards)
                if curr_count == prev_count:
                    break
                prev_count = curr_count

            # Collect project data
            property_cards = driver.find_elements(By.CSS_SELECTOR, ".project.approved.uc, .project.approved.r2m, .project.approvedundefined")

            if property_cards:
                for property_card in property_cards:
                    project_name = safe_get_text(property_card, ".p_detail .p_name")
                    developer = safe_get_text(property_card, ".p_detail .developer label")
                    rera = safe_get_text(property_card, ".p_detail .rera label")
                    location = safe_get_text(property_card, ".p_detail .info_col.location .lbl_value")
                    bedroom = safe_get_text(property_card, ".p_detail .info_col.bhk .lbl_value")

                    location_parts = location.split(",")
                    if len(location_parts) == 2:
                        locality, city_extracted = [part.strip() for part in location_parts]
                    else:
                        locality = location.strip()
                        city_extracted = city_name

                    writer.writerow([project_name, developer, rera, locality, city_extracted, bedroom, "ICICI BANK"])
                    time.sleep(0.3)
            else:
                print(f"No property cards found for city: {city_name}")

            # Go back to city selection
            driver.back()

            time.sleep(2)
            try:
                show_more_btn = driver.find_element(By.CSS_SELECTOR, "a.s_more")
                if show_more_btn.get_attribute("data-show-more-status") == "hidded":
                    driver.execute_script("arguments[0].click();", show_more_btn)
                    time.sleep(2)
            except Exception as e:
                print("No 'Show More' button found or already expanded:", e)

        except Exception as e:
            print(f"Error during search for {city_name}: {e}")
            continue

print("\nDone with all cities.")
driver.quit()
