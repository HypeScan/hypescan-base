import os, certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

import snscrape.modules.twitter as sntwitter

# ask for input
name = input("Enter a name or keyword to search: ").strip()

# build search query
query = f"{name}"

# scrape tweets
print(f"\nFetching tweets containing '{name}'...\n")
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    print(f"[{i+1}] {tweet.date} - @{tweet.user.username}")
    print(tweet.content)
    print("-" * 80)

    # limit output so it doesn’t go infinite
    if i >= 20:  # change 20 → any number you want
        break
