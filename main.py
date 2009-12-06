#!/usr/bin/env python

# PSL imports
import cgi
import logging
import os
import wsgiref.handlers
import xml.dom.minidom

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

class LogOutHander(webapp.RequestHandler):
  
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'token=;Max-Age=0')
    self.redirect('/')


def _get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc


class TweetHandler(webapp.RequestHandler):
  
  def post(self):
    user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
    key, secret = twitterutil.get_key_and_secret(user.user_id)

    response = twitterutil.set_status(self.request.get('tweet'), key, secret)
    res_doc = xml.dom.minidom.parseString(response)
    user_elem = res_doc.getElementsByTagName('user')[0]
    screen_name_elem = user_elem.getElementsByTagName('screen_name')[0]
    screen_name = _get_text(screen_name_elem.childNodes)
    self.redirect('http://twitter.com/%s' % screen_name)
    
def main():
  application = webapp.WSGIApplication([
      ('/', MainHandler),
      ('/logout', LogOutHander),
      ('/authenticate', twitteroauthhandlers.AuthenticateHandler),
      ('/tweet', TweetHandler),
      ('/oauth_callback', twitteroauthhandlers.CallbackHandler),
      ('/pubsub/add_subscription', pubsubhandlers.AddSubscriptionHandler),
      # Admin
      ('/admin/oauth_config', twitteroauthhandlers.OAuthConfigHandler),
      ('/admin/test_add_sub', pubsubhandlers.AddSubscriptionFormHandler),
      ('/admin/test_new_content_handler', pubsubhandlers.NewContentTestHandler)
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
