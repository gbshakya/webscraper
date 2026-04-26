import json
import os
from datetime import datetime
from sys import path
import time

# Add parent directory to path for imports
path.append(os.path.dirname(path[0]))
from collectDataJSON import scrape_company_details

# In-memory storage for serverless environment
cached_data = {
    "companies": [],
    "symbols": [],
    "last_updated": None,
    "metadata": {}
}

def load_symbols():
    """Load company symbols - in production, this could be from a database or API"""
    try:
        # For Vercel, we'll use hardcoded symbols initially
        symbols = [
            "NABIL", "NIMB", "SCB", "HBL", "SBI", "EBL", "NICA", "MBL", "LSL", "KBL",
            "SBL", "SHL", "TRH", "OHL", "NHPC", "BPCL", "CHCL", "STC", "BBC", "NUBL",
            "CBBL", "DDBL", "SANIMA", "NABBC", "NICL", "RBCL", "NLICL", "HEI", "UAIL",
            "SPIL", "NIL", "PRIN", "SALICO", "IGI", "NLIC", "LICN", "SICL", "NFS", "BNL"
        ]
        return symbols
    except Exception as e:
        print(f"Error loading symbols: {e}")
        return []

def initialize_cache():
    """Initialize cache with symbols and metadata"""
    global cached_data
    
    if not cached_data["symbols"]:
        cached_data["symbols"] = load_symbols()
        cached_data["metadata"] = {
            "total_symbols": len(cached_data["symbols"]),
            "data_source": "merolagani.com",
            "description": "Company financial data scraped from Merolagani",
            "version": "1.0",
            "environment": "serverless"
        }

def json_response(data, status_code=200):
    """Create JSON response for Vercel"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data, default=str)
    }

# API Route Functions

def home():
    """API Home - Basic info and available endpoints"""
    initialize_cache()
    return json_response({
        "message": "Nepal Stock Exchange Data API (Serverless)",
        "version": "1.0",
        "environment": "production",
        "endpoints": {
            "GET /": "API information",
            "GET /companies": "Get all company data",
            "GET /company/<symbol>": "Get specific company data",
            "GET /company/<symbol>/live": "Get live data for specific company",
            "GET /symbols": "Get all available symbols",
            "GET /sectors": "Get all available sectors",
            "POST /scrape": "Start fresh data scraping (limited)",
            "GET /scrape/status": "Get scraping status",
            "GET /health": "Health check"
        },
        "data_source": "merolagani.com",
        "cache_status": {
            "companies_count": len(cached_data["companies"]),
            "symbols_count": len(cached_data["symbols"]),
            "last_updated": cached_data["last_updated"]
        }
    })

def get_companies():
    """Get all company data with optional filtering"""
    try:
        companies = cached_data["companies"]
        
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
            "metadata": cached_data["metadata"],
            "companies": companies,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_company(symbol):
    """Get specific company data by symbol"""
    try:
        companies = cached_data["companies"]
        
        # Find company by symbol (case-insensitive)
        company = next((c for c in companies if c.get('symbol', '').upper() == symbol.upper()), None)
        
        if company:
            return jsonify(company)
        else:
            return jsonify({"error": f"Company '{symbol}' not found in cache"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

def get_symbols():
    """Get all available company symbols"""
    try:
        initialize_cache()
        return jsonify({
            "symbols": cached_data["symbols"],
            "total": len(cached_data["symbols"]),
            "source": "hardcoded_for_serverless"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sectors():
    """Get all available sectors"""
    try:
        companies = cached_data["companies"]
        
        # Extract unique sectors
        sectors = list(set(c.get('sector', 'Unknown') for c in companies if c.get('sector')))
        sectors.sort()
        
        return jsonify({
            "sectors": sectors,
            "total": len(sectors)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_scraping():
    """Start limited data scraping (serverless compatible)"""
    try:
        # In serverless, we can only scrape a few symbols due to timeout limits
        symbols = cached_data["symbols"][:5]  # Limit to first 5 symbols
        scraped_data = []
        
        for i, symbol in enumerate(symbols):
            try:
                company_data = scrape_company_details(symbol, i + 1)
                if company_data and company_data.get('symbol') != 'N/A':
                    scraped_data.append(company_data)
                time.sleep(1)  # Be polite to the server
            except Exception as e:
                print(f"Error scraping {symbol}: {e}")
                continue
        
        # Update cache with new data
        cached_data["companies"].extend(scraped_data)
        cached_data["last_updated"] = datetime.now().isoformat()
        
        return jsonify({
            "message": f"Scraped {len(scraped_data)} companies (limited for serverless)",
            "scraped_symbols": [c['symbol'] for c in scraped_data],
            "total_cached": len(cached_data["companies"])
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_scrape_status():
    """Get scraping status (simplified for serverless)"""
    return jsonify({
        "is_scraping": False,
        "environment": "serverless",
        "cache_status": {
            "companies_count": len(cached_data["companies"]),
            "symbols_count": len(cached_data["symbols"]),
            "last_updated": cached_data["last_updated"]
        },
        "note": "Full scraping not available in serverless environment"
    })

def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "serverless",
        "cache_status": {
            "companies_count": len(cached_data["companies"]),
            "symbols_count": len(cached_data["symbols"]),
            "last_updated": cached_data["last_updated"]
        }
    })

# Vercel serverless function entry point
def handler(request):
    """Main handler for Vercel serverless functions"""
    initialize_cache()
    
    # Parse request method and path from Vercel request
    method = request.method if hasattr(request, 'method') else 'GET'
    path = request.path if hasattr(request, 'path') else '/'
    
    # Handle query parameters
    if hasattr(request, 'query') and request.query:
        # Store query params for use in functions
        import types
        request.args = request.query
    else:
        request.args = {}
    
    print(f"Request: {method} {path}")  # Debug logging
    
    # Route the request
    if path == '/' or path == '':
        return home()
    elif path == '/companies':
        return get_companies()
    elif path.startswith('/company/'):
        parts = path.split('/')
        if len(parts) == 3:
            return get_company(parts[2])
        elif len(parts) == 4 and parts[3] == 'live':
            return get_company_live(parts[2])
    elif path == '/symbols':
        return get_symbols()
    elif path == '/sectors':
        return get_sectors()
    elif path == '/health':
        return health_check()
    elif path == '/scrape' and method == 'POST':
        return start_scraping()
    elif path == '/scrape/status':
        return get_scrape_status()
    
    print(f"Endpoint not found: {path}")  # Debug logging
    return jsonify({"error": f"Endpoint not found: {path}"}), 404
