#!/usr/local/bin/python3

import urllib.request
import json


"""
    Some constants and Facebook Access Token
"""

IMAGE_TYPE = 0
SEARCH_TYPE = 1
COVER_TYPE = 2
PICTURE = 'picture'
DATA = 'data'
URL = 'url'
COVER = 'cover'
SOURCE = 'source'
ID = 'id'
PAGING = 'paging'
NEXT = 'next'
GET = 'GET'
UTF8 = 'utf-8'
access_token = 'EAAF9oFQM9PUBAKldtWkKTW2mc5x1sVPhVPLrchgKA7meqkALAZCFkoDp3dqJilbcyT4DYRurqxZCDVssU1A9NHXEbV92QiH3Z'\
               'AnlDpYs2WdW6SQBrQpN46dHlMjBtOhVDKVfSOBUsHvxOmRqAmbiFZAUTgCKh4wZD'
urls = {SEARCH_TYPE: ('https://graph.facebook.com/search?q=', '&type=user&access_token=' + access_token),
        IMAGE_TYPE: ('https://graph.facebook.com/', '?fields=picture&access_token=' + access_token),
        COVER_TYPE: ('https://graph.facebook.com/', '?fields=cover&access_token=' + access_token)}


def get_url(query, _type):
    """
    Get the url the make a query
    :param query: The searched query
    :param _type: The type of the query: image, user of cover 
    :return: URL
    """
    return urls[_type][0] + query.replace(' ', '%20') + urls[_type][1]


def get_profile_pic(_id):
    """
    Gets the profile picture of a specific user
    :param _id: The ID of the user
    :return: The profile picture of the user
    """
    with urllib.request.urlopen(get_url(_id, IMAGE_TYPE)) as url:
        data = json.loads(url.read().decode())
    return data.get(PICTURE).get(DATA).get(URL)


def get_cover_photo(_id):
    """
    Gets the cover photo of a giver user
    :param _id: The ID of the user
    :return: The cover photo
    """
    with urllib.request.urlopen(get_url(_id, COVER_TYPE)) as url:
        data = json.loads(url.read().decode())
    if COVER not in data:
        return None
    if SOURCE not in data.get(COVER):
        return None
    return data.get(COVER).get(SOURCE)


def get_users_images(name, url=None):
    """
    Gets all images of the searched users
    :param name: Name of the user to be search
    :param url: URL in case of recursive search (NEXT attribute in JSON respons)
    :return: A tuple containing the user ID and the image (profile or cover)
    """
    if url is None:
        url = get_url(name, SEARCH_TYPE)
    with urllib.request.urlopen(url) as response:
        js = json.loads(response.read().decode())
        data = js[DATA]
    if data is None: return []
    for i in data:
        _id = i[ID]
        profile = get_profile_pic(_id=_id)
        cover = get_cover_photo(_id=_id)
        for image in (profile, cover):
            if image is not None: yield (_id, image)
    # Continue to next list
    if NEXT in js[PAGING]: yield from get_users_images(name, url=js[PAGING][NEXT])


def get_user_account(recognizer, name):
    """
    Gets the predicted account of the searched user
    :param recognizer: The recognizer object to predict the label
    :param name: The name of the user
    :return: The predicted user ID on Facebook
    """
    for user, image in get_users_images(name):
        if recognizer.is_valid_user(name, user, image, 'fb'):
            return user
