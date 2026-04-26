from bs4 import BeautifulSoup
import requests
import csv
import time
import os # Import the os module to check for file existence

# Path to the file containing company symbols
symbols_file = 'nepse_symbols.txt'

# Define the order of fields expected in the output CSV.
# These names are user-friendly for the CSV header.
# The mapping to actual website labels will be handled internally.
output_field_names = [
    "Symbol", "Sector", "Shares Outstanding", "Market Price", "Percent Change",
    "Last Trade On", "52 Week Low/High", "180 Day Average", "120 Day Average",
    "One Year Yield", "EPS", "P/E Ratio", "Book Value", "P/B Ratio",
    "Dividend", "180Change", "Technical Quality", "Fundamental Health", "Final Rating"
]

# Path for the output CSV file
output_csv_file = 'merolagani_company_info.csv'

def scrape_company_details(symbol , count):
    """
    Scrapes detailed financial information for a given company symbol from Merolagani.
    It attempts to find key-value pairs within tables on the company detail page. =(D2-H2)*100/H2

    Args:
        symbol (str): The stock symbol of the company (e.g., "NABIL").

    Returns:
        list: A list of scraped data values in the order of `output_field_names`,
              or a list filled with "N/A" if scraping fails.
    """
    mer_lagani_url = "https://merolagani.com/CompanyDetail.aspx?symbol="+symbol
    print(f"Fetching data for {count} : {symbol} from {mer_lagani_url}...")

    try:
        # Send a GET request to the URL with a timeout
        response = requests.get(mer_lagani_url, timeout=10)
        # Raise an HTTPError for bad responses (4xx or 5xx status codes)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Return a row with "N/A" for all fields if request fails
        return [symbol] + ["N/A"] * (len(output_field_names) - 1)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html5lib')
    tbody = soup.find_all("tbody")
    length=len(output_field_names) - 5  # Exclude the custom column from scraping
    rowToReturn = [symbol]
    for j in range(0,length):


        try:
            word = str(tbody[j].td.text)
            new = word.replace('\n','')
            striped = new.strip()
            rowToReturn.append(striped)
        except:
            rowToReturn.append("0")

    # Calculate 180Change: (Market Price - 180 Day Average) * 100 / 180 Day Average
    # Market Price is at index 3, 180 Day Average is at index 7
    try:
        market_price = float(rowToReturn[3])
        day_180_avg = float(rowToReturn[7])
        if day_180_avg != 0:
            change_180 = (market_price - day_180_avg) * 100 / day_180_avg
            rowToReturn.append(f"{change_180:.2f}")
        else:
            rowToReturn.append("0")
    except (ValueError, IndexError):
        rowToReturn.append("0")

    # Calculate Technical Quality: (Price - Low) / (High - Low)
    # where G (index 6) has format "High-Low"
    try:
        market_price = float(rowToReturn[3])
        low_high_range = rowToReturn[6]
        parts = low_high_range.split("-")
        if len(parts) == 2:
            high = float(parts[0])
            low = float(parts[1])
            denominator = low - high
            if denominator != 0:
                tech_quality = (market_price - high) / denominator
                rowToReturn.append(f"{tech_quality:.4f}")
            else:
                rowToReturn.append("0")
        else:
            rowToReturn.append("0")
    except (ValueError, IndexError):
        rowToReturn.append("0")

    # Calculate Fundamental Health: (0.4 * (1/P/E)) + (0.4 * (EPS/Price)) + (0.2 * (1/P/B))
    # K (index 10) = EPS, L (index 11) = P/E Ratio, N (index 13) = P/B Ratio, D (index 3) = Price
    try:
        market_price = float(rowToReturn[3])
        pe_ratio = float(rowToReturn[11])
        pb_ratio = float(rowToReturn[13])

        # Extract numeric value from EPS field (it may contain extra text like "(FY:...")
        eps_str = rowToReturn[10].split('(')[0].strip()
        eps_value = float(eps_str)

        health = 0
        if pe_ratio != 0:
            health += 0.4 * (1 / pe_ratio)
        if market_price != 0 and eps_value != 0:
            health += 0.4 * (eps_value / market_price)
        if pb_ratio != 0:
            health += 0.2 * (1 / pb_ratio)

        rowToReturn.append(f"{health:.4f}")
    except (ValueError, IndexError):
        rowToReturn.append("0")

    # Calculate Final Rating: (Technical Quality + Fundamental Health) / 2
    # Technical Quality at index -2, Fundamental Health at index -1 (after appending)
    try:
        tech_quality = float(rowToReturn[-2])
        fund_health = float(rowToReturn[-1])
        final_rating = (tech_quality + fund_health) / 2
        rowToReturn.append(f"{final_rating:.4f}")
    except (ValueError, IndexError):
        rowToReturn.append("0")

    return rowToReturn




# --- Main execution block ---
if __name__ == "__main__":
    print("Starting Merolagani Company Detail Scraper...")

    # Read company symbols from the file
    company_symbols = []
    if os.path.exists(symbols_file):
        try:
            with open(symbols_file, 'r', encoding='utf-8') as f:
                # Read each line, strip whitespace (including newlines), and add to list
                company_symbols = [line.strip() for line in f if line.strip()]

            print(f"Loaded {len(company_symbols)} symbols from '{symbols_file}'.")
        except IOError as e:
            print(f"Error reading symbols file '{symbols_file}': {e}")
            print("Exiting as no symbols could be loaded.")
            exit() # Exit if symbols can't be loaded
    else:
        print(f"Error: Symbols file '{symbols_file}' not found.")
        print("Please ensure 'nepse_symbols.txt' is in the same directory as the script.")
        print("Exiting.")
        exit() # Exit if file doesn't exist

    # Open the CSV file in write mode.
    # `newline=''` prevents extra blank rows in the CSV.
    # `encoding='utf-8'` ensures proper handling of various characters.
    try:
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
            the_writer = csv.writer(file)
            the_writer.writerow(output_field_names) # Write the header row

            # Iterate through each company symbol and scrape its details
            count = 1
            for symbol in company_symbols:
                # Skip empty symbols if any exist in the list (already handled by list comprehension, but good for safety)
                if not symbol.strip():
                    continue
                    
                company_data_row = scrape_company_details(symbol , count)
                count += 1
                if company_data_row: # Only write the row if data was successfully scraped
                    the_writer.writerow(company_data_row)
                    test = 2
                    
                time.sleep(1) # Be polite: Add a small delay between requests to avoid overwhelming the server

        print(f"\nScraping complete. Data saved to '{output_csv_file}'.")
        print(f"Total {len(company_symbols)} symbols processed.")

    except IOError as e:
        print(f"Error saving symbols to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during main execution: {e}")

