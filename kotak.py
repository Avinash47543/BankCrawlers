
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from urllib.parse import urljoin

def get_city_links(base_url):
    """Extract city links from the main page"""
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch the base URL: {base_url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    city_links = []
    tables = soup.find_all('table', class_='table-bordered')
    
    for table in tables:
        links = table.find_all('a')
        for link in links:
            city_name = link.text.strip()
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                city_links.append((city_name, full_url))
    
    return city_links

def extract_projects_data(city_url, city_name):
    """Extract project data from a city page"""
    print(f"Scraping data for {city_name} from {city_url}")
    
    response = requests.get(city_url)
    if response.status_code != 200:
        print(f"Failed to fetch the city page: {city_url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tables = soup.find_all('table', class_='table-bordered')
    if not tables:
        print(f"No table found for {city_name}")
        return []
    
    projects_data = []
    
    for table in tables:
        headers_row = table.find('tr')
        if not headers_row:
            continue
        
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                projects_data.append(row_data)
    
    return projects_data



def save_to_csv(projects_data, city_name, output_dir="kotak_approved_projects"):
    """Save projects data to a CSV file, always including headers"""
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.join(output_dir, f"{city_name.lower().replace(' ', '_')}_projects.csv")
    
    headers = ["Builder Name", "Project Name", "Location"]  # Fixed headers

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers first
        writer.writerow(headers)
        
        if projects_data:
            # Write the extracted data below headers
            writer.writerows(projects_data)
        else:
            print(f"No data found for {city_name}, only headers written.")
    
    print(f"Saved data for {city_name} to {filename}")

def main():
    base_url = "https://www.kotak.com/en/personal-banking/loans/home-loan/approved-housing-project-list.html"
    
    city_links = get_city_links(base_url)
    print(f"Found {len(city_links)} cities")
    
    output_dir = "kotak_approved_projects"
    os.makedirs(output_dir, exist_ok=True)
    
    for city_name, city_url in city_links:
        try:
            projects_data = extract_projects_data(city_url, city_name)
            save_to_csv(projects_data, city_name, output_dir)
            
            time.sleep(2)
        except Exception as e:
            print(f"Error processing {city_name}: {e}")
    
    print("Scraping completed!")

if __name__ == "__main__":
    main()
