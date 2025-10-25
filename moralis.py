import requests
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from typing import Optional, Dict

load_dotenv()
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
BASE_CHAIN = 'base'

class PricePercentChange(BaseModel):
    five_min: float
    one_hour: float
    four_hour: float
    twenty_four_hour: float

class LiquidityPercentChange(BaseModel):
    five_min: float
    one_hour: float
    four_hour: float
    twenty_four_hour: float

class Volume(BaseModel):
    five_min: float
    one_hour: float
    four_hour: float
    twenty_four_hour: float

class TokenData(BaseModel):
    tokenAddress: str
    tokenName: str
    tokenSymbol: str
    tokenLogo: Optional[str]
    pairCreated: str
    pairLabel: str
    pairAddress: str
    exchange: str
    exchangeAddress: str
    exchangeLogo: str
    exchangeUrl: str
    currentUsdPrice: str
    currentNativePrice: str
    totalLiquidityUsd: str
    pricePercentChange: PricePercentChange
    liquidityPercentChange: LiquidityPercentChange
    buys: Volume
    sells: Volume
    totalVolume: Volume
    buyVolume: Volume
    sellVolume: Volume
    buyers: Volume
    sellers: Volume

def fetch_token_price(pairAddress)->TokenData :
    url = f"https://deep-index.moralis.io/api/v2.2/pairs/{pairAddress}/stats?chain=base"
    
    headers = {
        "Accept": "application/json",
        "X-API-Key": MORALIS_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": str(err)}

if __name__ == "__main__":
    token_address = "0x98c8f03094a9e65ccedc14c40130e4a5dd0ce14fb12ea58cbeac11f662b458b9"
    price_data = fetch_token_price(token_address)
    print(json.dumps(price_data, indent=4)) 
    print(price_data)


