"""Handlers for OAuth authentication to Twitter."""

# PSL imports
import cgi
import logging
import os
import urllib2

# App Engine imports
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our imports
import models
import oauthutil
from third_party import oauth


class AuthenticateHandler(webapp.RequestHandler):
  """Implements the OAuth authentication flow for Twitter."""
  
  def get(self):
    """Get a request token from Twitter.

    Fetch a request token and redirect the user to Twitter authorization
    to authorize it for this app.  The callback is implemented by
    CallbackHandler.
    """

    consumer = oauthutil.get_consumer()
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

    # Save token so we can fetch it on callback.
    data_token = models.OAuthToken.get_or_insert(token.key, secret=token.secret)
    data_token.secret = token.secret
    data_token.put()
    
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
    consumer = oauthutil.get_consumer()

    # We're given the token, but need the secret we stored earlier
    token_param = self.request.get('oauth_token')
    data_token = models.OAuthToken.get_by_key_name(token_param)

    token = oauth.OAuthToken(token_param, data_token.secret)

    verifier = self.request.get('oauth_verifier')

    # Fetch the access token with this request token.
    access_token_url = 'http://twitter.com/oauth/access_token'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
      consumer, token=token, verifier=verifier, http_url=access_token_url)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
    response = urllib2.urlopen(oauth_request.to_url()).read()

    # Data comes back urlencoded in the body.
    data = cgi.parse_qs(response)

    # Save token data
    access_token = data['oauth_token'][0]
    user = models.TwitterUser.get_or_insert(
      access_token,
      secret = data['oauth_token_secret'][0],
      user_id = int(data['user_id'][0]),
      screen_name = data['screen_name'][0])
    user.put()

    # Set the cookie for the user so we can match it up later.
    self.response.headers.add_header('Set-Cookie', 'token=%s' % access_token)

    self.response.out.write('Successfully called back.  Saved token to cookie.')


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
