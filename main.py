import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any
import uvicorn
from services.moralis import fetch_token_price
from services.agents import moralis_crew
from services.models import TokenAnalysisResponse

app = FastAPI(
    title="HypeScan Token Analysis API",
    description="API for analyzing cryptocurrency tokens using Moralis data and CrewAI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analyze-token/{token_address}", response_model=TokenAnalysisResponse)
async def analyze_token(token_address: str):
    """
    Analyze a token's data using Moralis and CrewAI
    
    - **token_address**: The token's address or pair address to analyze
    """
    try:
        # 1️⃣ Fetch token data from Moralis
        print(f"Fetching token data for: {token_address} ...")
        price_data = fetch_token_price(token_address)

        if "error" in price_data:
            error_msg = f"Error fetching token data: {price_data['error']}"
            print(error_msg)
            return TokenAnalysisResponse(success=False, error=error_msg)

        print("\nRunning CrewAI Moralis analysis...")
        analysis_result = moralis_crew.kickoff(inputs={"data": price_data})
        
        # Convert to dict if it's a raw object
        if hasattr(analysis_result, 'raw'):
            analysis_result = analysis_result.raw

        # 3️⃣ Return the analysis output
        return TokenAnalysisResponse(
            success=True,
            data={
                "token_data": price_data,
                "analysis": analysis_result
            }
        )

    except Exception as e:
        error_msg = f"Error processing token analysis: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
