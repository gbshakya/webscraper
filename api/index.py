from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import os
from sys import path

# Add parent directory to path for imports
path.append(os.path.dirname(path[0]))

# In-memory storage for serverless environment
cached_data = {
    "companies": [],
    "symbols": [],
    "last_updated": None,
    "metadata": {}
}

def load_symbols():
    """Load company symbols - simplified for serverless"""
    try:
        # Hardcoded symbols for serverless environment
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

def get_home_response():
    """Home endpoint response - from app.py home()"""
    initialize_cache()
    return {
        "message": "Nepal Stock Exchange Data API",
        "version": "1.0",
        "environment": "serverless",
        "endpoints": {
            "GET /": "API information",
            "GET /companies": "Get all company data",
            "GET /company/<symbol>": "Get specific company data",
            "GET /company/<symbol>/live": "Get live data for specific company",
            "GET /symbols": "Get all available symbols",
            "GET /sectors": "Get all available sectors",
            "GET /health": "Health check",
            "GET /test": "Test endpoint"
        },
        "data_source": "merolagani.com",
        "cache_status": {
            "companies_count": len(cached_data["companies"]),
            "symbols_count": len(cached_data["symbols"]),
            "last_updated": cached_data["last_updated"]
        }
    }

def get_companies_response(query_params):
    """Companies endpoint response - from app.py get_companies()"""
    try:
        initialize_cache()
        companies = cached_data["companies"]
        
        # Optional query parameters for filtering
        sector = query_params.get('sector')
        limit = query_params.get('limit')
        offset = query_params.get('offset', '0')
        
        # Filter by sector if provided
        if sector:
            companies = [c for c in companies if c.get('sector', '').lower() == sector.lower()]
        
        # Apply pagination
        total = len(companies)
        if limit:
            try:
                limit = int(limit)
                offset = int(offset)
                companies = companies[offset:offset + limit]
            except ValueError:
                pass
        
        return {
            "metadata": cached_data["metadata"],
            "companies": companies,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }
    except Exception as e:
        return {"error": str(e)}

def get_company_response(symbol):
    """Company endpoint response - from app.py get_company()"""
    try:
        initialize_cache()
        companies = cached_data["companies"]
        
        # Find company by symbol (case-insensitive)
        company = next((c for c in companies if c.get('symbol', '').upper() == symbol.upper()), None)
        
        if company:
            return company
        else:
            return {"error": f"Company '{symbol}' not found"}
            
    except Exception as e:
        return {"error": str(e)}

def get_company_live_response(symbol):
    """Live company endpoint response - from app.py get_company_live()"""
    try:
        print(f"Fetching live data for {symbol}...")
        
        # Try to import the scraper - if fails, return error
        try:
            from collectDataJSON import scrape_company_details
            company_data = scrape_company_details(symbol, 1)
            
            if company_data and company_data.get('symbol') != 'N/A':
                return company_data
            else:
                return {"error": f"Could not fetch data for '{symbol}'"}
        except ImportError:
            return {"error": f"Live scraping not available in serverless environment for '{symbol}'"}
            
    except Exception as e:
        return {"error": str(e)}

def get_sectors_response():
    """Sectors endpoint response - from app.py get_sectors()"""
    try:
        initialize_cache()
        companies = cached_data["companies"]
        
        # Extract unique sectors
        sectors = list(set(c.get('sector', 'Unknown') for c in companies if c.get('sector')))
        sectors.sort()
        
        return {
            "sectors": sectors,
            "total": len(sectors)
        }
    except Exception as e:
        return {"error": str(e)}

def get_scrape_response():
    """Scrape endpoint response - from app.py start_scraping()"""
    try:
        initialize_cache()
        symbols = cached_data["symbols"][:5]  # Limit to first 5 symbols for serverless
        
        # Try to scrape limited data
        scraped_data = []
        try:
            from collectDataJSON import scrape_company_details
            for i, symbol in enumerate(symbols):
                try:
                    company_data = scrape_company_details(symbol, i + 1)
                    if company_data and company_data.get('symbol') != 'N/A':
                        scraped_data.append(company_data)
                except Exception as e:
                    print(f"Error scraping {symbol}: {e}")
                    continue
        except ImportError:
            return {"error": "Scraping not available in serverless environment"}
        
        # Update cache with new data
        cached_data["companies"].extend(scraped_data)
        cached_data["last_updated"] = "2026-04-26T12:00:00.000000"  # Simplified timestamp
        
        return {
            "message": f"Scraped {len(scraped_data)} companies (limited for serverless)",
            "scraped_symbols": [c['symbol'] for c in scraped_data],
            "total_cached": len(cached_data["companies"])
        }
        
    except Exception as e:
        return {"error": str(e)}

def get_scrape_status_response():
    """Scrape status endpoint response - from app.py get_scrape_status()"""
    initialize_cache()
    return {
        "is_scraping": False,
        "environment": "serverless",
        "cache_status": {
            "companies_count": len(cached_data["companies"]),
            "symbols_count": len(cached_data["symbols"]),
            "last_updated": cached_data["last_updated"]
        },
        "note": "Full scraping not available in serverless environment"
    }

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests - enhanced with app.py methods"""
        try:
            # Parse the path and query parameters
            path = self.path
            query = dict(parse.parse_qsl(parse.urlsplit(path).query))
            
            # Enhanced routing with app.py endpoints
            if path == '/' or path == '':
                response_data = get_home_response()
            elif path == '/companies':
                response_data = get_companies_response(query)
            elif path.startswith('/company/'):
                parts = path.split('/')
                if len(parts) == 3:
                    symbol = parts[2]
                    response_data = get_company_response(symbol)
                elif len(parts) == 4 and parts[3] == 'live':
                    symbol = parts[2]
                    response_data = get_company_live_response(symbol)
                else:
                    response_data = {"error": "Invalid company endpoint format"}
            elif path == '/symbols':
                initialize_cache()
                response_data = {
                    "symbols": cached_data["symbols"],
                    "total": len(cached_data["symbols"]),
                    "source": "hardcoded_for_serverless"
                }
            elif path == '/sectors':
                response_data = get_sectors_response()
            elif path == '/scrape/status':
                response_data = get_scrape_status_response()
            elif path == '/health':
                response_data = {
                    "status": "healthy",
                    "timestamp": "2026-04-26T12:00:00.000000",
                    "environment": "serverless",
                    "cache_status": {
                        "companies_count": len(cached_data["companies"]),
                        "symbols_count": len(cached_data["symbols"]),
                        "last_updated": cached_data["last_updated"]
                    }
                }
            elif path == '/test':
                response_data = {
                    "message": "Test successful!",
                    "path": path,
                    "query_params": query,
                    "user_agent": self.headers.get('User-Agent', 'Unknown')
                }
            else:
                response_data = {
                    "error": "Endpoint not found",
                    "path": path,
                    "available_endpoints": [
                        "/", "/companies", "/company/<symbol>", "/company/<symbol>/live",
                        "/symbols", "/sectors", "/scrape/status", "/health", "/test"
                    ]
                }
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data, indent=2).encode())
                return
            
            # Check if response contains an error
            if isinstance(response_data, dict) and 'error' in response_data:
                status_code = 404 if 'not found' in response_data['error'].lower() else 500
            else:
                status_code = 200
            
            # Send response
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2, default=str).encode())
            
        except Exception as e:
            # Send error response
            error_data = {
                "error": "Internal server error",
                "message": str(e),
                "path": self.path
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode())
    
    def do_POST(self):
        """Handle POST requests - enhanced with app.py methods"""
        try:
            # Parse the path
            path = self.path
            
            if path == '/scrape':
                response_data = get_scrape_response()
            else:
                # Read the request body for other POST requests
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                response_data = {
                    "message": "POST request received",
                    "path": path,
                    "headers": dict(self.headers),
                    "body_length": content_length,
                    "body": post_data.decode('utf-8', errors='ignore') if content_length > 0 else None
                }
            
            # Check if response contains an error
            if isinstance(response_data, dict) and 'error' in response_data:
                status_code = 500
            else:
                status_code = 200
            
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2, default=str).encode())
            
        except Exception as e:
            error_data = {
                "error": "Internal server error",
                "message": str(e),
                "path": self.path
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode())

# Export handler for Vercel
app = handler  # Vercel expects 'app' variable
application = handler  # Alternative name for some platforms
