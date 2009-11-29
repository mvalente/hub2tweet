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
import twitterutil
import twitteroauthhandlers


class MainHandler(webapp.RequestHandler):

  def get(self):
    user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
    text = template.render('templates/index.tpl', {
        'user': user
    })
    self.response.out.write(text)

def main():
  application = webapp.WSGIApplication([
      ('/', MainHandler),
      ('/authenticate', twitteroauthhandlers.AuthenticateHandler),
      ('/oauth_callback', twitteroauthhandlers.CallbackHandler),
      ('/admin/oauth_config', twitteroauthhandlers.OAuthConfigHandler)
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
