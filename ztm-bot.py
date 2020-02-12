# This file is for the Streaming tweepy API
# import time, tweepy, and the create_api function from config.py

# Create a class that accepts the tweepy.StreamListener

# Define an __init__ function inside the class that accepts self and api parameters

# Define an on_status function inside the class that accepts self and tweet parameters, retweet and favorite if the tweet has not been already

# Define an on_error function inside the class to catch errors

################### END OF CLASS ########################

# Define a main function that takes keywords and ids and connects to the tweepy stream api using those keywords and ids to track and follow

# if __name__ main define keywords to search for and ids to follow and run the main function with those

import tweepy

from config import create_api


class Stream_Listener(tweepy.StreamListener):
    """Defines the tweet status and error state

    """

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        """Checks the status of the tweet. Mark it as favourite if not already done it and retweet if not already
        retweeted.

        :param tweet: tweet from listening to the stream
        """
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except tweepy.TweepError as error:
                raise error
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except tweepy.TweepError as error:
                raise error

    def on_error(self, status_code):
        """When encountering an error while listening to the stream, return False if `status_code` is 420 and print
        the error.

        :param status_code:
        :return: False when `status_code` is 420 to disconnect the stream.
        """
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        print(tweepy.TweepError, status_code)


def main(follow, keyword):
    """Main method to initialize the api, create a Stream_Listener object to track tweets based on certain keywords and
    follow tweet owners and the mentors.
    """
    api = create_api()
    my_stream_listener = Stream_Listener(api)
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)

    follow_mentors = my_stream.filter(follow=follow)
    follow_keyword = my_stream.filter(track=keyword, is_async=True, languages=["en"])


if __name__ == '__main__':
    # The first is for Andrei Neagoie, The second for Yihua Zhang and the third for Daniel Bourke Yihua Zhang and the
    # third for Daniel Bourke
    follow_list = ["224115510", "2998698451", "743086819"]
    keywords = ["#ZTM", "#Zerotomastery", "#ztm", "zerotomastery", "ZeroToMastery"]
    main(follow_list, keywords)
