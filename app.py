from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from collectDataJSON import scrape_company_details
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
SYMBOLS_FILE = 'nepse_symbols.txt'
JSON_DATA_FILE = 'merolagani_company_info.json'

# Global variable to track scraping status
scraping_status = {
    "is_scraping": False,
    "progress": 0,
    "total": 0,
    "current_symbol": None,
    "start_time": None,
    "error": None
}

def load_company_data():
    """Load existing company data from JSON file"""
    try:
        if os.path.exists(JSON_DATA_FILE):
            with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"metadata": {}, "companies": []}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"metadata": {}, "companies": []}

def load_symbols():
    """Load company symbols from file"""
    try:
        if os.path.exists(SYMBOLS_FILE):
            with open(SYMBOLS_FILE, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        return []
    except Exception as e:
        print(f"Error loading symbols: {e}")
        return []

def scrape_all_companies():
    """Background function to scrape all companies"""
    global scraping_status
    
    try:
        scraping_status["is_scraping"] = True
        scraping_status["start_time"] = datetime.now().isoformat()
        scraping_status["error"] = None
        
        symbols = load_symbols()
        scraping_status["total"] = len(symbols)
        
        all_company_data = []
        dataset_metadata = {
            "scraped_at": datetime.now().isoformat(),
            "total_symbols": len(symbols),
            "data_source": "merolagani.com",
            "description": "Company financial data scraped from Merolagani",
            "version": "1.0"
        }
        
        for i, symbol in enumerate(symbols):
            if not symbol.strip():
                continue
                
            scraping_status["current_symbol"] = symbol
            scraping_status["progress"] = i + 1
            
            try:
                company_data = scrape_company_details(symbol, i + 1)
                if company_data:
                    all_company_data.append(company_data)
                time.sleep(1)  # Be polite to the server
            except Exception as e:
                print(f"Error scraping {symbol}: {e}")
                continue
        
        # Save final data
        final_json = {
            "metadata": dataset_metadata,
            "companies": all_company_data
        }
        
        with open(JSON_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_json, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        scraping_status["error"] = str(e)
        print(f"Scraping error: {e}")
    finally:
        scraping_status["is_scraping"] = False
        scraping_status["current_symbol"] = None

# API Routes

@app.route('/', methods=['GET'])
def home():
    """API Home - Basic info and available endpoints"""
    return jsonify({
        "message": "Nepal Stock Exchange Data API",
        "version": "1.0",
        "endpoints": {
            "GET /": "API information",
            "GET /companies": "Get all company data",
            "GET /company/<symbol>": "Get specific company data",
            "GET /symbols": "Get all available symbols",
            "POST /scrape": "Start fresh data scraping",
            "GET /scrape/status": "Get scraping status"
        },
        "data_source": "merolagani.com"
    })

@app.route('/companies', methods=['GET'])
def get_companies():
    """Get all company data with optional filtering"""
    try:
        data = load_company_data()
        companies = data.get("companies", [])
        
        # Optional query parameters for filtering
        sector = request.args.get('sector')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        # Filter by sector if provided
        if sector:
            companies = [c for c in companies if c.get('sector', '').lower() == sector.lower()]
        
        # Apply pagination
        total = len(companies)
        if limit:
            companies = companies[offset:offset + limit]
        
        return jsonify({
            "metadata": data.get("metadata", {}),
            "companies": companies,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/company/<symbol>', methods=['GET'])
def get_company(symbol):
    """Get specific company data by symbol"""
    try:
        data = load_company_data()
        companies = data.get("companies", [])
        
        # Find company by symbol (case-insensitive)
        company = next((c for c in companies if c.get('symbol', '').upper() == symbol.upper()), None)
        
        if company:
            return jsonify(company)
        else:
            return jsonify({"error": f"Company '{symbol}' not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/company/<symbol>/live', methods=['GET'])
def get_company_live(symbol):
    """Get live data for a specific company (fresh scrape)"""
    try:
        print(f"Fetching live data for {symbol}...")
        company_data = scrape_company_details(symbol, 1)
        
        if company_data and company_data.get('symbol') != 'N/A':
            return jsonify(company_data)
        else:
            return jsonify({"error": f"Could not fetch data for '{symbol}'"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/symbols', methods=['GET'])
def get_symbols():
    """Get all available company symbols"""
    try:
        symbols = load_symbols()
        return jsonify({
            "symbols": symbols,
            "total": len(symbols),
            "source_file": SYMBOLS_FILE
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape', methods=['POST'])
def start_scraping():
    """Start fresh data scraping process"""
    global scraping_status
    
    if scraping_status["is_scraping"]:
        return jsonify({
            "message": "Scraping already in progress",
            "status": scraping_status
        }), 400
    
    # Start scraping in background thread
    thread = threading.Thread(target=scrape_all_companies)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "message": "Scraping started",
        "status": scraping_status
    })

@app.route('/scrape/status', methods=['GET'])
def get_scrape_status():
    """Get current scraping status"""
    return jsonify(scraping_status)

@app.route('/sectors', methods=['GET'])
def get_sectors():
    """Get all available sectors"""
    try:
        data = load_company_data()
        companies = data.get("companies", [])
        
        # Extract unique sectors
        sectors = list(set(c.get('sector', 'Unknown') for c in companies if c.get('sector')))
        sectors.sort()
        
        return jsonify({
            "sectors": sectors,
            "total": len(sectors)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_file_exists": os.path.exists(JSON_DATA_FILE),
        "symbols_file_exists": os.path.exists(SYMBOLS_FILE)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Nepal Stock Exchange Data API...")
    print("API will be available at: http://localhost:5000")
    print("Available endpoints:")
    print("  GET /companies - Get all company data")
    print("  GET /company/<symbol> - Get specific company data")
    print("  GET /company/<symbol>/live - Get live data for specific company")
    print("  GET /symbols - Get all available symbols")
    print("  GET /sectors - Get all available sectors")
    print("  POST /scrape - Start fresh data scraping")
    print("  GET /scrape/status - Get scraping status")
    print("  GET /health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
