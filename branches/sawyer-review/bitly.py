import sys
import urllib2

from django.utils import simplejson

_BITLY_API_KEY = 'R_8b57834cbee48f8419e98bf7af03f4d4'

def get_shortened_url(url):
  """Shorten the given URL with the Bitly API."""
  version = '2.0.1'
  login = 'nanaze'
  bitly_url= "http://api.bit.ly/shorten?version=%s&longUrl=%s&login=%s&apiKey=%s" % (version, url, login, _BITLY_API_KEY)
  response = urllib2.urlopen(bitly_url).read()
  json = simplejson.loads(response)
  return json['results'].values()[0]['shortUrl']

def main():
  """Run bitly as a command line tool.  Prints out a shortened url."""
  print get_shortened_url(sys.argv[1])

if __name__ == '__main__':
  main()
