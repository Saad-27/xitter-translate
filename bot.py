# bot.py
import tweepy
from googletrans import Translator
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

translator = Translator()

LANG_MAP = {
    "french": "fr",
    "spanish": "es",
    "german": "de",
}

def translate_tweet(tweet_text, lang_code):
    return translator.translate(tweet_text, dest=lang_code).text

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            if status.in_reply_to_status_id is not None:

                original_tweet = api.get_status(status.in_reply_to_status_id)
                tweet_text = original_tweet.text

                # Check if the tweet has the correct mention format
                if '@tranlatebot27 translate to' in status.text.lower():
                    lang_keyword = status.text.lower().split("translate to")[1].strip().split()[0]
                    lang_code = LANG_MAP.get(lang_keyword, None)

                    if lang_code:
                        translated_text = translate_tweet(tweet_text, lang_code)
                        response = f"@{status.user.screen_name} Translated to {lang_keyword}:\n{translated_text}"
                    else:
                        response = f"@{status.user.screen_name} Sorry, I don't support that language."

                    # Post the response as a reply
                    api.update_status(status=response, in_reply_to_status_id=status.id)
        except Exception as e:
            print(f"Error: {e}")

    def on_error(self, status_code):
        if status_code == 420:
            return False

if __name__ == "__main__":
    # Create a stream listener
    listener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    # Start the stream, listening for mentions
    stream.filter(track=["@tranlatebot27"])
