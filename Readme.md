# HypeScan 🚀

HypeScan is a powerful cryptocurrency analysis platform that provides real-time token analysis, social sentiment tracking, and market insights. Built with FastAPI and leveraging multiple data sources including Moralis and Twitter, it offers comprehensive analytics for crypto traders and enthusiasts.

## Features

- **Token Analysis**: In-depth analysis of cryptocurrency tokens using Moralis data
- **Social Sentiment**: Track Twitter mentions and sentiment for tokens
- **Market Data**: Real-time price, volume, and liquidity metrics
- **AI-Powered Insights**: CrewAI integration for intelligent analysis and reporting
- **RESTful API**: Easy integration with other applications

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Data Sources**: Moralis API, Twitter API, Bitquery
- **AI/ML**: CrewAI for intelligent analysis
- **Deployment**: Uvicorn ASGI server

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip
- API keys for Moralis, Twitter, and Bitquery

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HypeScan/hypescan-base.git
   cd hypescan-base
   ```

2. Install dependencies:
   ```bash
   # Using poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload

# Access the API documentation at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## API Endpoints

- `GET /api/analyze-token/{token_address}` - Analyze a token's data
- `GET /health` - Health check endpoint

## Services

### Token Analysis Service
Located in `services/moralis.py`, this service handles fetching and processing token data from Moralis API.

### AI Analysis
Uses CrewAI in `services/agents.py` to provide intelligent insights and analysis of token data.

### Twitter Integration
Social sentiment analysis through Twitter data collection and processing.

## Development

### Project Structure

```
hypescan-base/
├── services/           # Core services
│   ├── agents.py      # AI analysis with CrewAI
│   ├── models.py      # Pydantic models
│   └── moralis.py     # Moralis API integration
├── main.py            # FastAPI application
├── bitq.py            # Bitquery integration
├── gmgn_crawler.py    # GMGN crawler
├── scrape.py          # Social media scraping
└── requirements.txt   # Dependencies
```

### Environment Variables

Create a `.env` file with the following variables:

```
MORALIS_API_KEY=your_moralis_api_key
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password
BITQUERY_API_KEY=your_bitquery_api_key
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Moralis](https://moralis.io/) for blockchain data
- [CrewAI](https://github.com/joaomdmoura/crewAI) for AI-powered analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## Contact

For any questions or suggestions, please open an issue or contact the maintainers.
