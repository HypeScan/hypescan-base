import os
from typing import Optional, Dict, Any
from pydantic import BaseModel
import requests
from datetime import datetime


class BitqueryResponse(BaseModel):
    data: Dict[str, Any]
    status: str
    error: Optional[str] = None


class BitqueryAPI:
    """
    Bitquery API client for fetching token information
    """
    
    def __init__(self, api_key: Optional[str] = None, oauth_token: Optional[str] = None):
        """
        Initialize Bitquery API client
        
        Args:
            api_key: API key for V1 API (from X-API-KEY header)
            oauth_token: OAuth token for V2 Streaming API
        """
        self.api_key = api_key or os.getenv("BITQUERY_API_KEY")
        self.oauth_token = oauth_token or os.getenv("BITQUERY_OAUTH_TOKEN")
        
        # V1 API endpoint
        self.v1_endpoint = "https://graphql.bitquery.io/"
        
        # V2 Streaming API endpoint
        self.v2_endpoint = "https://streaming.bitquery.io/graphql"
    
    def get_v1_headers(self) -> Dict[str, str]:
        """Get headers for V1 API"""
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }
    
    def get_v2_headers(self) -> Dict[str, str]:
        """Get headers for V2 API"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.oauth_token}"
        }
    
    def get_token_holders(
        self, 
        token_address: str, 
        network: str = "eth",
        limit: int = 100,
        date: Optional[str] = None
    ) -> BitqueryResponse:
        """
        Fetch top token holders using V2 API
        
        Args:
            token_address: The token contract address
            network: Blockchain network (eth, bsc, polygon, etc.)
            limit: Number of top holders to fetch
            date: Date for historical data (YYYY-MM-DD format)
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            query = """
            query ($network: evm_network!, $token: String!, $limit: Int!, $date: String!) {
              EVM(dataset: archive, network: $network) {
                TokenHolders(
                  date: $date
                  tokenSmartContract: $token
                  limit: {count: $limit}
                  orderBy: {descending: Balance_Amount}
                  where: {Balance: {Amount: {gt: "0"}}}
                ) {
                  Holder {
                    Address
                  }
                  Balance {
                    Amount
                  }
                }
              }
            }
            """
            
            variables = {
                "network": network,
                "token": token_address,
                "limit": limit,
                "date": date
            }
            
            payload = {
                "query": query,
                "variables": variables
            }
            
            response = requests.post(
                self.v2_endpoint,
                headers=self.get_v2_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return BitqueryResponse(
                    data=data,
                    status="success"
                )
            else:
                return BitqueryResponse(
                    data={},
                    status="error",
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return BitqueryResponse(
                data={},
                status="error",
                error=str(e)
            )
    
    def get_token_holder_stats(
        self,
        token_address: str,
        network: str = "eth",
        date: Optional[str] = None
    ) -> BitqueryResponse:
        """
        Get token holder statistics including Gini coefficient and Nakamoto coefficient
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            query = """
            query ($network: evm_network!, $token: String!, $date: String!) {
              EVM(dataset: archive, network: $network) {
                TokenHolders(
                  tokenSmartContract: $token
                  date: $date
                  where: {Balance: {Amount: {gt: "0"}}}
                ) {
                  gini(of: Balance_Amount)
                  nakamoto(of: Balance_Amount, percent: 0.51)
                  theil(of: Balance_Amount)
                  uniq(of: Holder_Address)
                  sum(of: Balance_Amount)
                  average(of: Balance_Amount)
                  median(of: Balance_Amount)
                }
              }
            }
            """
            
            variables = {
                "network": network,
                "token": token_address,
                "date": date
            }
            
            payload = {
                "query": query,
                "variables": variables
            }
            
            response = requests.post(
                self.v2_endpoint,
                headers=self.get_v2_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return BitqueryResponse(
                    data=data,
                    status="success"
                )
            else:
                return BitqueryResponse(
                    data={},
                    status="error",
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return BitqueryResponse(
                data={},
                status="error",
                error=str(e)
            )
    
    def get_token_transfers(
        self,
        token_address: str,
        network: str = "eth",
        limit: int = 100,
        since_date: Optional[str] = None
    ) -> BitqueryResponse:
        """
        Get recent token transfers
        """
        try:
            if since_date is None:
                # Last 7 days by default
                from datetime import timedelta
                since = datetime.now() - timedelta(days=7)
                since_date = since.strftime("%Y-%m-%d")
            
            query = """
            query ($network: evm_network!, $token: String!, $limit: Int!, $since: String!) {
              EVM(dataset: combined, network: $network) {
                Transfers(
                  limit: {count: $limit}
                  orderBy: {descending: Block_Time}
                  where: {
                    Transfer: {Currency: {SmartContract: {is: $token}}}
                    Block: {Date: {since: $since}}
                  }
                ) {
                  Transfer {
                    Amount
                    Sender
                    Receiver
                    Currency {
                      Name
                      Symbol
                    }
                  }
                  Block {
                    Time
                    Number
                  }
                  Transaction {
                    Hash
                  }
                }
              }
            }
            """
            
            variables = {
                "network": network,
                "token": token_address,
                "limit": limit,
                "since": since_date
            }
            
            payload = {
                "query": query,
                "variables": variables
            }
            
            response = requests.post(
                self.v2_endpoint,
                headers=self.get_v2_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return BitqueryResponse(
                    data=data,
                    status="success"
                )
            else:
                return BitqueryResponse(
                    data={},
                    status="error",
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return BitqueryResponse(
                data={},
                status="error",
                error=str(e)
            )
    
    def get_dex_trades(
        self,
        token_address: str,
        network: str = "eth",
        limit: int = 100,
        since_date: Optional[str] = None
    ) -> BitqueryResponse:
        """
        Get DEX trades for a token
        """
        try:
            if since_date is None:
                from datetime import timedelta
                since = datetime.now() - timedelta(days=7)
                since_date = since.strftime("%Y-%m-%d")
            
            query = """
            query ($network: evm_network!, $token: String!, $limit: Int!, $since: String!) {
              EVM(dataset: combined, network: $network) {
                DEXTrades(
                  limit: {count: $limit}
                  orderBy: {descending: Block_Time}
                  where: {
                    Trade: {
                      Buy: {Currency: {SmartContract: {is: $token}}}
                    }
                    Block: {Date: {since: $since}}
                  }
                ) {
                  Block {
                    Time
                    Number
                  }
                  Transaction {
                    Hash
                  }
                  Trade {
                    Buy {
                      Amount
                      Buyer
                      Currency {
                        Name
                        Symbol
                      }
                      Price
                    }
                    Sell {
                      Amount
                      Seller
                      Currency {
                        Name
                        Symbol
                      }
                      Price
                    }
                    Dex {
                      ProtocolName
                      ProtocolFamily
                    }
                  }
                }
              }
            }
            """
            
            variables = {
                "network": network,
                "token": token_address,
                "limit": limit,
                "since": since_date
            }
            
            payload = {
                "query": query,
                "variables": variables
            }
            
            response = requests.post(
                self.v2_endpoint,
                headers=self.get_v2_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return BitqueryResponse(
                    data=data,
                    status="success"
                )
            else:
                return BitqueryResponse(
                    data={},
                    status="error",
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            return BitqueryResponse(
                data={},
                status="error",
                error=str(e)
            )


async def get_bitquery_info(
    token_address: str, 
    network: str = "eth",
    api_key: Optional[str] = None,
    oauth_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch comprehensive token information from Bitquery
    
    Args:
        token_address: The token address to look up
        network: Blockchain network (eth, bsc, polygon, base, etc.)
        api_key: Bitquery API key (optional, will use env var)
        oauth_token: Bitquery OAuth token (optional, will use env var)
        
    Returns:
        Dictionary containing all token data
    """
    try:
        client = BitqueryAPI(api_key=api_key, oauth_token=oauth_token)
        
        # Fetch all data
        holders_response = client.get_token_holders(token_address, network)
        stats_response = client.get_token_holder_stats(token_address, network)
        transfers_response = client.get_token_transfers(token_address, network)
        trades_response = client.get_dex_trades(token_address, network)
        
        # Combine all responses
        result = {
            "token_address": token_address,
            "network": network,
            "top_holders": holders_response.data if holders_response.status == "success" else None,
            "holder_statistics": stats_response.data if stats_response.status == "success" else None,
            "recent_transfers": transfers_response.data if transfers_response.status == "success" else None,
            "dex_trades": trades_response.data if trades_response.status == "success" else None,
            "errors": []
        }
        
        # Collect any errors
        if holders_response.status == "error":
            result["errors"].append(f"Holders: {holders_response.error}")
        if stats_response.status == "error":
            result["errors"].append(f"Stats: {stats_response.error}")
        if transfers_response.status == "error":
            result["errors"].append(f"Transfers: {transfers_response.error}")
        if trades_response.status == "error":
            result["errors"].append(f"Trades: {trades_response.error}")
        
        return result
        
    except Exception as e:
        return {
            "token_address": token_address,
            "network": network,
            "error": str(e),
            "status": "failed"
        }