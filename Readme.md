# HypeScan: Advanced Cryptocurrency Analysis Platform 

HypeScan is a sophisticated cryptocurrency analysis platform that combines on-chain data, social sentiment, and AI-powered insights to provide comprehensive token analysis. Built with FastAPI and leveraging multiple data sources including Moralis, Bitquery, and Gemini AI, it offers traders and investors deep insights into token metrics and market trends.

## Key Features

- **Comprehensive Token Analysis**: In-depth analysis using Moralis API for on-chain data
- **AI-Powered Insights**: Advanced analysis using CrewAI and Gemini 1.5 Pro
- **Social Sentiment**: Twitter sentiment analysis and community engagement metrics
- **Security Analysis**: GMGN.ai integration for token security assessment
- **Real-time Market Data**: Price, volume, liquidity, and holder analysis
- **Predictive Analytics**: AI-driven price movement predictions

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: 
  - CrewAI for multi-agent analysis
  - Gemini 1.5 Pro for advanced reasoning
  - Multiple LLM integration (Llama 3, DeepSeek)
- **Data Sources**:
  - Moralis API
  - Bitquery
  - GMGN.ai
  - Twitter API
- **Deployment**: Uvicorn ASGI server
- **Containerization**: Docker support

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip
- Required API keys (see Configuration)

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

3. Install Playwright for browser automation:
   ```bash
   playwright install
   ```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your API keys:
   ```
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key
   
   # Optional but recommended
   MORALIS_API_KEY=your_moralis_api_key
   BITQUERY_API_KEY=your_bitquery_api_key
   ```

## Project Structure

```
hypescan-base/
├── services/
│   ├── agents.py       # AI analysis agents and tasks
│   ├── models.py       # Pydantic models and schemas
│   ├── moralis.py      # Moralis API integration
│   └── gemini.py       # Gemini AI integration
├── bitq.py             # Bitquery integration
├── gmgn_crawler.py     # GMGN.ai data collection
├── main.py             # FastAPI application entry point
└── requirements.txt    # Python dependencies
```

## Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

## API Endpoints

### Token Analysis
- `GET /api/analyze-token/{token_address}`
  - Analyzes a token using multiple data sources
  - Returns comprehensive analysis including price, volume, and AI insights

### System Health
- `GET /health` - Service health check

## AI Analysis Pipeline

HypeScan uses a multi-agent system powered by CrewAI:

1. **Data Analyzer**: Processes raw token metrics and market data
2. **GMGN Analyzer**: Evaluates token safety and security metrics
3. **Twitter Analyzer**: Assesses social sentiment and community engagement
4. **Prediction Agent**: Provides buy/sell/hold recommendations

## Security

- All sensitive data is stored in environment variables
- API keys are never hardcoded in the source
- Input validation using Pydantic models
- Rate limiting (coming soon)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgements

- [Moralis](https://moralis.io/) for blockchain data
- [CrewAI](https://github.com/joaomdmoura/crewAI) for AI-powered analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## Contact

For inquiries or support, please open an issue on GitHub or contact the maintainers.
