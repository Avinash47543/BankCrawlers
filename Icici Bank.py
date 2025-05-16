import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()

url = "https://home.icicibank.com/home?ITM=nli_cms_hlbt_productnavigation_Approved-Projects"
driver.get(url)
wait = WebDriverWait(driver, 10)

def safe_get_text(el, selector):
    try:
        return el.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return "N/A"

otp_done = False

city_input = wait.until(EC.element_to_be_clickable((By.ID, "txtCity")))
city_input.click()
time.sleep(2)

city_elements = driver.find_elements(By.CSS_SELECTOR, ".bropbox.drop_box li")
city_names = [el.text.strip() for el in city_elements if el.text.strip()]

print(f"Found {len(city_names)} cities.")

with open("icici_bank_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Project Name", "Builder Name", "RERA No.", "Location", "City", "Bedroom", "Bank"])

    for city_index, city_name in enumerate(city_names):
        print(f"Searching for: {city_name}")

        city_input = wait.until(EC.element_to_be_clickable((By.ID, "txtCity")))
        city_input.click()
        time.sleep(1.5)

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

        try:
            search_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSearch_new")))
            search_btn.click()

            if not otp_done:
                print("Please enter your mobile number and OTP manually on the browser.")
                input("Press ENTER here after OTP verification is complete and results are loaded... ")
                otp_done = True

            prev_count = 0

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                cards = driver.find_elements(By.CSS_SELECTOR, ".project.approved.uc, .project.approved.r2m, .project.approvedundefined")
                curr_count = len(cards)

                if curr_count == prev_count:
                    break

                prev_count = curr_count

            property_cards=driver.find_elements(By.CSS_SELECTOR,".project.approved.uc, .project.approved.r2m, .project.approvedundefined")

            if property_cards:

                    for property_card in property_cards:
                        project_name = safe_get_text(property_card, ".p_detail .p_name")
                        developer = safe_get_text(property_card, ".p_detail .developer label")
                        rera = safe_get_text(property_card, ".p_detail .rera label")
                        location = safe_get_text(property_card, ".p_detail .info_col.location .lbl_value")
                        bedroom = safe_get_text(property_card, ".p_detail .info_col.bhk .lbl_value")

                        location_parts = location.split(",")
                        if len(location_parts) == 2:
                            locality, city = [part.strip() for part in location_parts]
                        else:
                            locality = location.strip()
                            city = city_name

                        time.sleep(0.5)

                        writer.writerow([project_name,developer,rera,locality, city, bedroom, "ICICI BANK"])

                    time.sleep(2)

            else:
                print(f"No property Card Found")

            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"Error during search for {city_name}: {e}")
            continue

print("Done with all cities.")
driver.quit()
