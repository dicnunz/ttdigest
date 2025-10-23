import snscrape.modules.twitter as sntwitter
import openai

# configure your OpenAI key here
openai.api_key = "YOUR_OPENAI_API_KEY"

def fetch_latest_tweets(username, max_tweets=5):
    tweets = []
    for tweet in sntwitter.TwitterUserScraper(username).get_items():
        tweets.append(tweet)
        if len(tweets) >= max_tweets:
            break
    return tweets

def summarize_text(text, model="gpt-3.5-turbo", max_tokens=150):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "Summarize the following tweet thread in concise bullet points."},
                  {"role": "user", "content": text}],
        max_tokens=max_tokens,
        temperature=0.5)
    return response.choices[0].message["content"].strip()

if __name__ == "__main__":
    seed_accounts = ["alliekmiller", "mattshumer_", "OfficialLoganK", "drfeifei", "AndrewYNg",
                     "jeremyphoward", "demishassabis", "ylecun", "karpathy"]
    for account in seed_accounts:
        tweets = fetch_latest_tweets(account, max_tweets=3)
        for tw in tweets:
            summary = summarize_text(tw.content)
            print(f"Summary for @{account}: {summary}\n")
