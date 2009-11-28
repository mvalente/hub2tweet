"""Handlers for OAuth authentication to Twitter."""

# PSL imports
import os
import urllib2

# App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our imports
import models
from third_party import oauth

def _get_consumer_key_and_secret():
  """Pull the key and secret from datastore."""
  configs = models.OAuthConfig.all()

  if configs.count():
    config = configs[0]
    return config.consumer_key, config.consumer_secret


class AuthenticateHandler(webapp.RequestHandler):
  """Implements the OAuth authentication flow for Twitter."""
  
  def get(self):
    """Get a request token from Twitter.

    Fetch a request token and redirect the user to Twitter authorization
    to authorize it for this app.  The callback is implemented by
    CallbackHandler.
    """

    auth_tuple = _get_consumer_key_and_secret()
    if not auth_tuple:
      self.response.out.write('Keys not configured.')
      return

    key, secret = auth_tuple
    consumer = oauth.OAuthConsumer(key, secret)

    req_url = 'http://twitter.com/oauth/request_token'
    # Make callback relative to working server.
    # Particularly for localhost when running locally.
    callback_url = 'http://%s/oauth_callback' % os.environ['HTTP_HOST']

    # Build request token request.
    req = oauth.OAuthRequest.from_consumer_and_token(
      consumer, callback=callback_url, 
      http_url= req_url)
    signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method_hmac_sha1, consumer, None)

    # Get request token from Twitter.
    response = urllib2.urlopen(req.to_url()).read()
    token = oauth.OAuthToken.from_string(response)

    # Build authentication token request
    auth_url = 'http://twitter.com/oauth/authorize'
    req = oauth.OAuthRequest.from_token_and_callback(
      token=token,
      http_url=auth_url)
    req.sign_request(signature_method_hmac_sha1, consumer, token)

    # Redirect user to get authentication token.
    self.redirect(req.to_url())


class CallbackHandler(webapp.RequestHandler):
  """Handles the callback from the Twitter OAuth authenticator."""
  def get(self):
    self.response.out.write('Successfully called back.  TODO: properly handle.')


class OAuthConfigHandler(webapp.RequestHandler):
  """Admin interface for setting application OAuth keys."""

  def get(self):
    """Write out the current keys and a form to change them."""
    values = {}

    auth_tuple = _get_consumer_key_and_secret()
    if auth_tuple:
      values['consumer_key'], values['consumer_secret'] = auth_tuple

    text = template.render('templates/oauthconfig.tpl', values)
    self.response.out.write(text)
    
  def post(self):
    """Make a new config from POST and have it replace all other configs."""
    new_config = models.OAuthConfig(
      consumer_key = self.request.get('consumer_key'),
      consumer_secret = self.request.get('consumer_secret'))

    # Remove all other configs.
    for config in models.OAuthConfig.all():
      config.delete()

    new_config.put()

    self.redirect('/admin/oauth_config')


