import asyncio
from x import search_twitter, SearchType

async def main():
    # If you have a Twitter account and want to log in, fill these
    TWITTER_USERNAME="productiseai"
    TWITTER_PASSWORD="p~2k^-@R%?zg_Bb"
    username = TWITTER_USERNAME
    password = TWITTER_PASSWORD

    response = await search_twitter(
        query="DOGE",
        search_type=SearchType.LATEST,  # LATEST, TOP, PEOPLE, PHOTOS, VIDEOS
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
