# Nepal Stock Exchange Data Scraper API

A Flask-based API for scraping Nepal Stock Exchange data from Merolagani, with support for both local development and Vercel serverless deployment.

## Features

- **RESTful API** with JSON responses
- **Live data scraping** from Merolagani
- **Company financial metrics** (P/E ratio, technical analysis, etc.)
- **Serverless compatible** for Vercel deployment
- **CORS enabled** for web integration
- **Background scraping** with progress tracking (local only)

## Local Development

### Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the local server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

- `GET /` - API information
- `GET /companies` - Get all company data
- `GET /company/<symbol>` - Get specific company data
- `GET /company/<symbol>/live` - Get live data for specific company
- `GET /symbols` - Get all available symbols
- `GET /sectors` - Get all available sectors
- `POST /scrape` - Start fresh data scraping
- `GET /scrape/status` - Get scraping status
- `GET /health` - Health check

## Vercel Deployment

### Prerequisites

- Vercel account
- GitHub repository with this code

### Deployment Steps

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy to Vercel**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

3. **Environment Variables** (optional):
   - Set any required environment variables in Vercel dashboard

### Vercel Limitations

- **No file persistence**: Data is cached in memory only
- **Limited scraping**: Only 5 companies per request due to timeout limits
- **No background tasks**: Scraping is synchronous in serverless functions
- **Function timeouts**: Vercel functions have execution time limits

### Production Considerations

For production use with Vercel, consider:

1. **Database Integration**: Replace file storage with a database (Vercel KV, Supabase, etc.)
2. **External Scraping Service**: Use a separate service for heavy scraping tasks
3. **Caching Strategy**: Implement Redis or similar for better performance
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Monitoring**: Add error tracking and monitoring

## API Response Format

### Company Data Example
```json
{
  "symbol": "NABIL",
  "sector": "Commercial Banks",
  "market_price": "518.00",
  "pe_ratio": "14.72",
  "technical_quality": "0.4835",
  "fundamental_health": "0.1452",
  "final_rating": "0.3144",
  "scraped_at": "2026-04-26T11:59:37.440483"
}
```

## Data Source

- **Primary**: Merolagani (https://merolagani.com)
- **Symbols**: Nepal Stock Exchange listed companies

## Technical Stack

- **Backend**: Flask (Python)
- **Scraping**: BeautifulSoup, Selenium
- **Deployment**: Vercel Serverless Functions
- **Data Format**: JSON

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is for educational and research purposes. Please respect the terms of service of the data sources.
