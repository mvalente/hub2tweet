import sys
import urllib2

from django.utils import simplejson

_BITLY_API_KEY = 'R_8b57834cbee48f8419e98bf7af03f4d4'

def get_shortened_url(url):
  """Shorten the given URL with the Bitly API."""
  
  # TODO(sawyer): Fill this in.  Use urllib2 to fetch the JSON object
  # and simplejson to parse out the shortened URL.
  # See http://code.google.com/p/bitly-api/wiki/ApiDocumentation and
  # http://simplejson.googlecode.com/svn/tags/simplejson-2.0.9/docs/index.html

def main():
  """Run bitly as a command line tool.  Prints out a shortened url."""
  print get_shortened_url(sys.argv[1])

if __name__ == '__main__':
  main()
