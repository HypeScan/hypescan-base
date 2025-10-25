import asyncio
import json
from services.moralis import fetch_token_price
from services.agents import moralis_crew

# Example: replace with your token address
TOKEN_ADDRESS = "0x98c8f03094a9e65ccedc14c40130e4a5dd0ce14fb12ea58cbeac11f662b458b9"

async def main():
    # 1️⃣ Fetch token data from Moralis
    print(f"Fetching token data for: {TOKEN_ADDRESS} ...")
    price_data = fetch_token_price(TOKEN_ADDRESS)

    if "error" in price_data:
        print("Error fetching token data:", price_data["error"])
        return

    # Optional: pretty print fetched token data
    print("\nFetched token data:")
    print(json.dumps(price_data, indent=4))

    print("\nRunning CrewAI Moralis analysis...")
    analysis_result = moralis_crew.kickoff(inputs={"data": price_data})

    # 3️⃣ Print the analysis output
    print("\n===== CREWAI TOKEN ANALYSIS OUTPUT =====")
    print(analysis_result)
    analysis_result = analysis_result.raw

    # 4️⃣ Save the result to JSON file
    with open("moralis_token_analysis_result.json", "w") as f:
        json.dump(analysis_result, f, indent=4)
    print("\nAnalysis saved to: moralis_token_analysis_result.json")

# Run the async main
if __name__ == "__main__":
    asyncio.run(main())
