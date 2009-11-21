#!/usr/bin/env python

# PSL imports
import os
import wsgiref.handlers

# App Engine imports
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

# Our imports
from third_party import oauth
import models

# This is filled in in main()
OAUTH_CLIENT = None

class MainHandler(webapp.RequestHandler):

  def get(self):
    text = template.render('templates/index.tpl', {})
    self.response.out.write(text)


class AuthenticateHandler(webapp.RequestHandler):
  """Redirects the user to Twitter's OAuth authenticator."""
  def get(self):
    self.redirect(OAUTH_CLIENT.get_authorization_url())


class CallbackHandler(webapp.RequestHandler):
  """Handles the callback from the Twitter OAuth authenticator."""
  def get(self):
    # TODO(nanaze): Properly handle here.  Right now, just show that we got
    # here.
    self.response.out.write('callback handler')


def main():

  host = os.environ['HTTP_HOST']

  # Make the callback url be this server.
  callback_url = 'http://%s/oauth_callback' % host

  # Set the global OAUTH_CLIENT singleton, and have it call back to this server.
  # We use the first config in the datastore.
  config = models.OAuthConfig.all()[0]
  global OAUTH_CLIENT
  OAUTH_CLIENT = oauth.TwitterClient(
    config.consumer_key, config.consumer_secret, callback_url)

  application = webapp.WSGIApplication([
      ('/', MainHandler),
      ('/authenticate', AuthenticateHandler),
      ('/oauth_callback', CallbackHandler)
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
