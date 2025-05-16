from selenium import webdriver
from selenium.webdriver.common.by import By
import csv, time

driver = webdriver.Chrome()

url = "https://www.sbirealty.in/property-in-gurugram"
driver.get(url)
driver.maximize_window()

prev_count = 0

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    cards = driver.find_elements(By.CSS_SELECTOR, ".project.approved")
    curr_count = len(cards)

    if curr_count == prev_count:
        break

    prev_count = curr_count

print(f"Total properties loaded: {curr_count}")

property_cards = driver.find_elements(By.CSS_SELECTOR, ".project.approved")

if property_cards:

    with open("sbi_reality_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Rera Number", "Project Name", "Developer", "Location", "BHK", "Price"])

        seen_projects = set()

        for eachProperty in property_cards:
            if not eachProperty.is_displayed():
                continue

            try:

                try:
                    pname = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .p_name").text.strip()
                except:
                    pname = "N/A"

                try:
                    reraNumber = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .rera_cn label").text.strip()
                except:
                    reraNumber = "N/A"

                unique_id = f"{pname.lower().strip()}|{reraNumber.lower().strip()}"
                if unique_id in seen_projects:
                    continue
                seen_projects.add(unique_id)

                try:
                    dev = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .developer").text.strip()
                except:
                    dev = "N/A"

                try:
                    loc = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .location").text.strip()
                except:
                    loc = "N/A"

                try:
                    bhk = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .bhk").text.strip()
                except:
                    bhk = "N/A"

                try:
                    price = eachProperty.find_element(By.CSS_SELECTOR, ".p_detail .c_bottom .price").text.strip()
                except:
                    price = "N/A"

                writer.writerow([reraNumber, pname, dev, loc, bhk, price])

            except Exception as e:
                print(f"Skipping one property due to outer error: {e}")

    print(f"Unique properties written to CSV: {len(seen_projects)}")

else:
    print("No Data Found!!! Sorry")

driver.quit()
