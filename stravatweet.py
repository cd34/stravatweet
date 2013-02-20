#!/usr/bin/env python

"""
Uses: http://code.google.com/p/python-weather-api/
      https://github.com/Packetslave/strava
      https://github.com/tweepy/tweepy/
      https://github.com/cd34/birdcage
"""

import os.path
import sys
import ConfigParser

import pywapi

from strava import Athlete
import tweepy
import webhelpers.date
from birdcage import (Phrase,
                      Text)

def tweet(message, config):
    auth = tweepy.OAuthHandler(config.get('StravaTweet', 'consumer_key'), 
        config.get('StravaTweet', 'consumer_secret'))
    auth.set_access_token(config.get('StravaTweet', 'access_key'), 
        config.get('StravaTweet', 'access_secret'))
    api = tweepy.API(auth)
    api.update_status(message)

def segment_message(num_segments):
    message = ''
    if num_segments > 0:
        message = '(%d segments)' % num_segments
    if num_segments == 1:
        message = '(%d segment)' % num_segments
    return message

def build_message(ride, units, config):

    text_distance = 'miles'
    text_speed = 'mph'
    distance = ride.detail.distance * 0.000621
    speed = ride.detail.average_speed * 2.24543081
    if units == 'metric':
        text_distance = 'kms'
        text_speed = 'kmh'
        distance = ride.detail.distance / 1000
        speed = ride.detail.average_speed * 3.6
    
    message_preamble = Text('I rode')
    message_speed = Text('%.1f %s @ %.1f %s' % (distance, text_distance, 
        speed, text_speed))
    message_duration = get_duration(ride.detail.moving_time)
    message_with_strava = Text('with @strava', 'w/ @strava')
    message_segment = Text(segment_message(len(ride.segments)))
    message_wind = Text(get_wind(config.get('StravaTweet', 'zip'), 
        config.get('StravaTweet', 'unit')))

    hashtags = Text(*[x.strip() for x in config.get('StravaTweet', 'hashtags') \
            .split(',')])

    message = Phrase(message_preamble, message_speed, message_duration,
        message_with_strava, message_segment, message_wind, hashtags) \
        .generate(length=118) + ' http://app.strava.com/rides/%s' % ride.id
    return(message)

def last_tweeted_id(ride_id, config):
    f = open(os.path.join(config.get('StravaTweet', 'workdir'), 
        'lastid.txt'), 'a+')
    last_id = int(f.readline() or 0)
    if ride_id > last_id:
        f.seek(0)
        f.truncate(0)
        f.write('%s' % ride_id)
        f.close()
        return False
    else:
        return True

def get_wind_direction(direction):
    compass_headings = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    return compass_headings[int(int(direction)/45)]

def get_wind(zip, units):
    weather = pywapi.get_weather_from_yahoo(zip)
    wind = 'No wind'
    if weather['wind']['speed'] > 1:
        wind = 'Wind %dmph from %s' % (float(weather['wind']['speed']), \
               get_wind_direction(weather['wind']['direction']))
    return wind

def get_duration(moving_time):
    long_time = 'in ' + webhelpers.date.distance_of_time_in_words(moving_time,
               granularity='minute').replace(' and', ',')
    short_time = long_time.replace('minutes', 'mins').replace('hours', 'hrs')
    return Text(long_time, short_time)

def getstats(config):
    st = Athlete(config.get('StravaTweet', 'rider'))
    lastride = st.rides()[0]
    if last_tweeted_id(lastride.id, config):
        return None
    else:
        return build_message(lastride, config.get('StravaTweet', 'unit'), 
            config)

if __name__ == "__main__":
    try:
        config = ConfigParser.RawConfigParser()
        config.read('stravatweet.cfg')

        tweet_message = getstats(config)
        if tweet_message:
            tweet(tweet_message, config)
            print tweet_message
    except KeyboardInterrupt:
        sys.exit()
