#!/usr/local/bin/python3

import tweepy

"""
    Parameters for Twitter API
"""

CONSUMER_KEY = '2xxdblpINV1olRDCo8IzyDsjH'
CONSUMER_SECRET = 'Wsp9ZmNWRUAgPcspOclniHoSy6BXhmJtdGzzjZaJ0HLCdfRerm'
ACCESS_TOKEN = '838315910041587712-K602r8Iao0sRt5Ezu82LgCfUKeK7UsV'
ACCESS_TOKEN_SECRET = 'gvQCPRGSKlpvVr9wkpWXXihSWmxP8V8q59JqweX51RqVM'

"""
    Twitter API object 
"""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_users_images(name):
    """
    Gets the list of images of the searched user
    :param name: The name of the user to be searched
    :return: A list containing (username, image)
    """
    users = api.search_users(name)
    l = []
    for u in users:
        l.append((u.screen_name, str(u.profile_image_url).replace('_normal', '')))
    return l


def get_user_account(recognizer, name,):
    """
    Get the predicted username of the user on Twitter
    :param recognizer: The recognizer object to predict the label
    :param name: Name of the user to be searched
    :return: The predicted Twitter username of the user
    """
    for user, image in get_users_images(name):
        if recognizer.is_valid_user(name, user, image, platform='tw'):
            return user
