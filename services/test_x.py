import asyncio
from x import search_twitter, SearchType

async def main():
    username = "productiseai"
    password = "p~2k^-@R%?zg_Bb"

    response = await search_twitter(
        query="DOGE",
        search_type=SearchType.LATEST,
        max_tweets=5,
        username=username,
        password=password
    )

    if response.status == "success":
        for tweet in response.tweets:
            print(f"{tweet.user.screen_name}: {tweet.text}\n")
    else:
        print("Error:", response.error)

asyncio.run(main())
