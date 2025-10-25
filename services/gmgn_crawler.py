# import asyncio
# import json
# import re
# from typing import Optional
# from bs4 import BeautifulSoup
# from pydantic import BaseModel
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# class GMGNResponse(BaseModel):
#     token_name: Optional[str] = None
#     price: Optional[str] = None
#     fdv: Optional[str] = None
#     holders: Optional[str] = None
#     liquidity: Optional[str] = None
#     status: str
#     error: Optional[str] = None

# async def get_gmgn_info(token_address: str) -> GMGNResponse:
#     url = f"https://gmgn.ai/base/token/VIVOWmEQ_{token_address}"

#     try:
#         browser_config = BrowserConfig(
#             headless=True,
#             verbose=False,
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/120.0.0.0 Safari/537.36"
#             )
#         )

#         run_config = CrawlerRunConfig(cache_mode="bypass")

#         async with AsyncWebCrawler(config=browser_config) as crawler:
#             # wait_for ensures JS-heavy pages render fully
#             result = await crawler.arun(url, config=run_config, wait_for=6)

#             if not result or not result.html:
#                 return GMGNResponse(status="error", error="Empty HTML response")

#             soup = BeautifulSoup(result.html, "html.parser")
#             text = soup.get_text(" ", strip=True)

#             def extract(label: str):
#                 match = re.search(rf"{label}[:\s]*([\d.,$A-Za-z]+)", text)
#                 return match.group(1) if match else None

#             return GMGNResponse(
#                 token_name=extract("Name"),
#                 price=extract("Price"),
#                 fdv=extract("FDV"),
#                 holders=extract("Holders"),
#                 liquidity=extract("Liquidity"),
#                 status="success",
#             )

#     except Exception as e:
#         return GMGNResponse(status="error", error=str(e))

# async def main():
#     token_address = "0xd85c31854c2B0Fb40aaA9E2Fc4Da23C21f829d46"
#     response = await get_gmgn_info(token_address)
#     print(json.dumps(response.model_dump(), indent=4))

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import os
import json
from typing import Optional, Dict, Any
from pydantic import BaseModel
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

class GMGNResponse(BaseModel):
    markdown: str
    status: str
    error: Optional[str] = None

async def get_gmgn_info(token_address: str) -> GMGNResponse:
    """
    Fetch token information from GMGN.ai
    
    Args:
        token_address: The token address to look up
        
    Returns:
        GMGNResponse object containing the markdown data and status
    """
    try:
        url = f"https://gmgn.ai/base/token/{token_address}"
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url)
            
            if not result or not result.markdown:
                return GMGNResponse(
                    markdown="",
                    status="error",
                    error="Failed to fetch data from GMGN.ai"
                )
            
            return GMGNResponse(
                markdown=result.markdown,
                status="success"
            )
            
    except Exception as e:
        return GMGNResponse(
            markdown="",
            status="error",
            error=str(e)
        )

async def main():
    token_address = "0x4200000000000000000000000000000000000006"
    response = await get_gmgn_info(token_address)
    print(json.dumps(response.model_dump(), indent=4))

if __name__ == "__main__":
    asyncio.run(main())
