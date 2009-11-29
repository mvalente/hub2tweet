"""Utility methods for posting to Twitter."""

import urllib2

import oauthutil
import models

from third_party import oauth

def get_user_by_token_key(key):
  """Gets the TwitterUser object associated with the given key name."""
  return models.TwitterUser.get_by_key_name(key)

def set_status_by_user_id(status, user_id):
  """Set a status by user id.  ID is expected to be in the datastore."""
  key, secret = get_key_and_secret(user_id)
  set_status(status, key, secret)

def get_key_and_secret(user_id):
  """Get the OAuth token key and secret for the given user id from the datastore."""
  query = models.TwitterUser.all()
  query.filter('user_id =', user_id)
  user = query.get()
  return user.key().name(), user.secret

def set_status(status, oauth_token, oauth_secret):
  """Set a Twitter status.

  Args:
    status: New Tweet, ideally < 140 characters.
    oauth_token: Access token.
    oauth_secret: Access token secret.
  """

  consumer = oauthutil.get_consumer()
  token = oauth.OAuthToken(oauth_token, oauth_secret)

  update_url = 'http://twitter.com/statuses/update.xml'
  oauth_request = oauth.OAuthRequest.from_consumer_and_token(
    consumer, token=token, http_method='POST', http_url=url, parameters=parameters)

  # POST signing isn't working.  It apparently works to just put the request as part
  # of the query string.
  oauth_request.set_parameter('status', status)
  oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
  
  # This request actually posts the Tweet.
  urllib2.urlopen(oauth_request.to_url(), '')
