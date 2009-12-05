#!/usr/bin/env python

# PSL imports
import cgi
import logging
import os
import wsgiref.handlers

# App Engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our imports
import models
import pubsubhandlers
import twitterutil
import twitteroauthhandlers


class MainHandler(webapp.RequestHandler):

  def get(self):
    values = {}
    if 'token' in self.request.cookies:
      user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
      values['user'] = user


    text = template.render('templates/index.tpl', values)

    self.response.out.write(text)

def main():
  application = webapp.WSGIApplication([
      ('/', MainHandler),
      ('/authenticate', twitteroauthhandlers.AuthenticateHandler),
      ('/oauth_callback', twitteroauthhandlers.CallbackHandler),
      ('/pubsub/add_subscription', pubsubhandlers.AddSubscriptionHandler),
      # Admin
      ('/admin/oauth_config', twitteroauthhandlers.OAuthConfigHandler),
      ('/admin/test_add_sub', pubsubhandlers.AddSubscriptionFormHandler),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
