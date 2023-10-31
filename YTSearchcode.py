# YoutubeSearchCode

# Includes
import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

# From # https://github.com/youtube/api-samples/blob/master/python/search.py: 
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Read config file as a file object configdat
with open('config.py', 'r') as configdat:
    s = configdat.readline().strip().split(',')
# Note that .readline is a method associated with file objects. Each time called it
# reads a new line. Other file object methods are .read(), .write() and .close()
# To make the list without the while you could use:
# configdat = open('config.py')
# s = configdat.readline().strip()  # Read the first line and strip whitespace
# configdat.close()  # Don't forget to close the file!
# t = s.split(',')  # Split the stripped string by commas. Now t is the list.

DEVELOPER_KEY = s[0]
searchterm1 = s[1]
searchterm2 = s[2]
print(DEVELOPER_KEY, searchterm1, searchterm2)

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
# This is from # https://github.com/youtube/api-samples/blob/master/python/search.py

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Create a local database and tables # This is from class spider.py
# Must still figure out how to get the desired data from YT to populate it.

conn = sqlite3.connect('YTsearchcode.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Creator
    (id INTEGER PRIMARY KEY, name TEXT UNIQUE, followers INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Video
    (id INTEGER PRIMARY KEY, title TEXT UNIQUE, uniqueID TEXT UNIQUE, views INTEGER,
            creator_id INTEGER)''')



# Source of this code to get statistics on BBC channel is a youtube tutorial 
# video at https://www.youtube.com/watch?v=TIZRskDMyA4

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  
# Make a request to Youtube API. Use youtube variable just created and add parameters 
# from youtube documentation at https://developers.google.com/youtube/v3/docs/channels/list
request = youtube.channels().list(
    part = 'statistics',
    forUsername = 'BBCNews'
)

# Get a response from the API and print it
response = request.execute()
print(response)