from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Selenium
service = Service('c:\Windows\chromedriver.exe')
driver = webdriver.Chrome(service=service)

def scrape_company_symbols():
    try:
        # Load the NEPSE company page
        driver.get("https://www.nepalstock.com/company")
        
        all_symbols = []
        page_count = 0
        
        while True:
            # Wait for the table to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )
            
            # Find all rows in the table body
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            
            # Extract symbols from current page
            page_symbols = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    page_symbols.append(cols[2].text.strip())
            
            all_symbols.extend(page_symbols)
            page_count += 1
            print(f"Scraped {len(page_symbols)} symbols from page {page_count}")
            
            # Check for and click next page button
            print(driver.page_source)  # Debugging line to see the current page source
            try:
                next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.pagination-next a"))
                )
                parent_li = next_button.find_element(By.XPATH, "..") # Get the parent <li>

                if "pagination-next" not in parent_li.get_attribute("class") or not next_button.is_enabled():
                    print("Reached the last page or 'Next' button is not active.")
                    break

                # Click the next button
                next_button.click()
               
                
        
                time.sleep(3)  # Wait for page to load
            except Exception as e:
                print(f"Could not find next button: {e}")
                break
                
        return all_symbols
    
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    
    finally:
        driver.quit()

# Run the scraper
company_symbols = scrape_company_symbols()

# Save results to a file
with open("nepse_symbols.txt", "w") as f:
    f.write("\n".join(company_symbols))

print("\nAll company symbols:")
print("\n".join(company_symbols))
print(f"\nTotal {len(company_symbols)} company symbols collected")
print("Results saved to 'nepse_symbols.txt'")