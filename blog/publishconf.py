import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

AUTHOR = 'THM'
SITESUBTITLE = '...'
SITENAME = 'Team THM'
SITEURL = 'https://artefactory.github.io/redis-team-THM/'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
