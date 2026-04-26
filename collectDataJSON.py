from bs4 import BeautifulSoup
import requests
import json
import time
import os
from datetime import datetime

# Path to the file containing company symbols
symbols_file = 'nepse_symbols.txt'

# Define the field names for JSON output
output_field_names = [
    "symbol", "sector", "shares_outstanding", "market_price", "percent_change",
    "last_trade_on", "week_52_low_high", "day_180_average", "day_120_average",
    "one_year_yield", "eps", "pe_ratio", "book_value", "pb_ratio",
    "dividend", "change_180", "technical_quality", "fundamental_health", "final_rating"
]

# Path for the output JSON file
output_json_file = 'merolagani_company_info.json'

def scrape_company_details(symbol, count):
    """
    Scrapes detailed financial information for a given company symbol from Merolagani.
    Returns structured data as a dictionary for JSON output.

    Args:
        symbol (str): The stock symbol of the company (e.g., "NABIL").
        count (int): The current count for progress tracking.

    Returns:
        dict: A dictionary containing scraped company data with proper field names.
    """
    mer_lagani_url = f"https://merolagani.com/CompanyDetail.aspx?symbol={symbol}"
    print(f"Fetching data for {count} : {symbol} from {mer_lagani_url}...")

    try:
        # Send a GET request to the URL with a timeout
        response = requests.get(mer_lagani_url, timeout=10)
        # Raise an HTTPError for bad responses (4xx or 5xx status codes)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Return a dictionary with "N/A" for all fields if request fails
        return {field: "N/A" for field in output_field_names}

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html5lib')
    tbody = soup.find_all("tbody")
    
    # Initialize result dictionary with symbol
    result = {"symbol": symbol}
    
    # Extract basic data from tbody elements
    field_mapping = [
        "sector", "shares_outstanding", "market_price", "percent_change",
        "last_trade_on", "week_52_low_high", "day_180_average", "day_120_average",
        "one_year_yield", "eps", "pe_ratio", "book_value", "pb_ratio", "dividend"
    ]
    
    for i, field in enumerate(field_mapping):
        try:
            if i < len(tbody):
                word = str(tbody[i].td.text)
                cleaned = word.replace('\n', '').strip()
                result[field] = cleaned
            else:
                result[field] = "N/A"
        except:
            result[field] = "N/A"

    # Calculate 180Change: (Market Price - 180 Day Average) * 100 / 180 Day Average
    try:
        market_price = float(result["market_price"])
        day_180_avg = float(result["day_180_average"])
        if day_180_avg != 0:
            change_180 = (market_price - day_180_avg) * 100 / day_180_avg
            result["change_180"] = f"{change_180:.2f}"
        else:
            result["change_180"] = "0"
    except (ValueError, KeyError):
        result["change_180"] = "0"

    # Calculate Technical Quality: (Price - Low) / (High - Low)
    # where week_52_low_high has format "High-Low"
    try:
        market_price = float(result["market_price"])
        low_high_range = result["week_52_low_high"]
        parts = low_high_range.split("-")
        if len(parts) == 2:
            high = float(parts[0])
            low = float(parts[1])
            denominator = low - high
            if denominator != 0:
                tech_quality = (market_price - high) / denominator
                result["technical_quality"] = f"{tech_quality:.4f}"
            else:
                result["technical_quality"] = "0"
        else:
            result["technical_quality"] = "0"
    except (ValueError, KeyError):
        result["technical_quality"] = "0"

    # Calculate Fundamental Health: (0.4 * (1/P/E)) + (0.4 * (EPS/Price)) + (0.2 * (1/P/B))
    try:
        market_price = float(result["market_price"])
        pe_ratio = float(result["pe_ratio"])
        pb_ratio = float(result["pb_ratio"])

        # Extract numeric value from EPS field (it may contain extra text like "(FY:...")
        eps_str = result["eps"].split('(')[0].strip()
        eps_value = float(eps_str)

        health = 0
        if pe_ratio != 0:
            health += 0.4 * (1 / pe_ratio)
        if market_price != 0 and eps_value != 0:
            health += 0.4 * (eps_value / market_price)
        if pb_ratio != 0:
            health += 0.2 * (1 / pb_ratio)

        result["fundamental_health"] = f"{health:.4f}"
    except (ValueError, KeyError):
        result["fundamental_health"] = "0"

    # Calculate Final Rating: (Technical Quality + Fundamental Health) / 2
    try:
        tech_quality = float(result["technical_quality"])
        fund_health = float(result["fundamental_health"])
        final_rating = (tech_quality + fund_health) / 2
        result["final_rating"] = f"{final_rating:.4f}"
    except (ValueError, KeyError):
        result["final_rating"] = "0"

    # Add metadata
    result["scraped_at"] = datetime.now().isoformat()
    result["data_source"] = "merolagani.com"
    
    return result


# --- Main execution block ---
if __name__ == "__main__":
    print("Starting Merolagani Company Detail Scraper (JSON Output)...")

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
            exit()
    else:
        print(f"Error: Symbols file '{symbols_file}' not found.")
        print("Please ensure 'nepse_symbols.txt' is in the same directory as the script.")
        print("Exiting.")
        exit()

    # Initialize list to store all company data
    all_company_data = []
    
    # Add metadata for the entire dataset
    dataset_metadata = {
        "scraped_at": datetime.now().isoformat(),
        "total_symbols": len(company_symbols),
        "data_source": "merolagani.com",
        "description": "Company financial data scraped from Merolagani",
        "version": "1.0"
    }

    # Iterate through each company symbol and scrape its details
    count = 1
    for symbol in company_symbols:
        if not symbol.strip():
            continue
            
        company_data = scrape_company_details(symbol, count)
        count += 1
        
        if company_data:
            all_company_data.append(company_data)
            
        time.sleep(1)  # Be polite: Add a small delay between requests

    # Create final JSON structure
    final_json = {
        "metadata": dataset_metadata,
        "companies": all_company_data
    }

    # Save to JSON file
    try:
        with open(output_json_file, 'w', encoding='utf-8') as file:
            json.dump(final_json, file, indent=2, ensure_ascii=False)
        
        print(f"\nScraping complete. Data saved to '{output_json_file}'.")
        print(f"Total {len(company_symbols)} symbols processed.")
        print(f"Successfully scraped {len(all_company_data)} companies.")
        
        # Print sample data for verification
        if all_company_data:
            print(f"\nSample data for {all_company_data[0]['symbol']}:")
            sample = {k: v for k, v in all_company_data[0].items() if k not in ['scraped_at', 'data_source']}
            print(json.dumps(sample, indent=2))
            
    except IOError as e:
        print(f"Error saving data to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during main execution: {e}")
