"""Handlers for subscriptions."""

import os
import urllib
import urllib2
import random
import xml.dom.minidom
import logging

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

import bitly
import feeds
import models
import twitterutil


def _get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc

def _get_msg(title, url):
  link_short = bitly.get_shortened_url(url)
  title_short = title[0:140 - (1+len(link_short))]
  msg = "%s %s" % (title_short, link_short)
  return msg

def _get_verify_token():
  chars = []
  for i in range(32):
    chars.append(random.choice('0123456789ABCDEF'))
  return ''.join(chars)
  
class AddSubscriptionHandler(webapp.RequestHandler):
  
  def post(self):
    user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
    feed_url = self.request.get('feed')
    callback_url = 'http://%s/pubsub' % os.environ['HTTP_HOST']
    xml_doc = urllib2.urlopen(feed_url).read()
    feed = xml.dom.minidom.parseString(xml_doc).getElementsByTagName('feed')[0]
    hub_link = feeds.get_hub(feed)
    self_link = feeds.get_self(feed)

    # If debug on localhost, we can't actually get verification from the
    # server.  So hit the hub async and pretend we verified.
    debug = os.environ['HTTP_HOST'].startswith('localhost')

    verify_token = _get_verify_token()
    params = {
      'hub.callback': callback_url,
      'hub.mode': 'subscribe',
      'hub.topic': self_link, 
      'hub.verify': 'sync' if not debug else 'async',
      'hub.verify_token' : verify_token
    }
    data = urllib.urlencode(params)

    # Make sure to add the subscription before hitting the hub.
    sub = models.TopicSubscription(user_id=user.user_id, topic=self_link,
                                   verify_token=verify_token, verified=debug)
    sub.put() 

    response = urlfetch.fetch(hub_link, payload=data, method='POST')
    if response.status_code not in [202, 204]:
      self.error(502)
      self.response.out.write('Error registering with hub. ')
      self.response.out.write('Status code response: %s. ' % response.status_code)
      self.response.out.write(response.content)
      return

    self.redirect('/')

class PubSubHandler(webapp.RequestHandler):

  def post(self):
    self.handle_atom_feed(self.request.body)

  def handle_atom_feed(self, atom):
    xml_doc = xml.dom.minidom.parseString(atom)

    feed = xml_doc.getElementsByTagName('feed')[0]
    # Use this later
    feed_url = feeds.get_self(feed)

    logging.info('Self: %s' % feed_url)

    key, secret = twitterutil.get_key_and_secret(91536090) # hard-code hub2tweet for now

    entries = feed.getElementsByTagName('entry')
    for entry in entries:
      entry_url = feeds.get_web_link(entry)

      title_element = entry.getElementsByTagName('title')[0]
      title = _get_text(title_element.childNodes)
      msg = _get_msg(title, entry_url)
      twitterutil.set_status(msg, key, secret)
      self.response.out.write('sent tweet ' + msg)


  def get(self):
    """Handler for verification."""
    query = models.TopicSubscription.all()
    query.filter('topic = ', self.request.get('hub.topic'))
    query.filter('verify_token = ', self.request.get('hub.verify_token'))
    
    topic = query.get()
    
    if not topic:
      self.error(404)
      self.response.out.write(
        'Topic subscription doesn\'t exist or was deleted')
      return

    topic.verified = True
    topic.put()

    # Hub wants us to echo back its challenge string to verify success.
    self.response.out.write(self.request.get('hub.challenge'))

class AddSubscriptionFormHandler(webapp.RequestHandler):

  def get(self):
   self.response.out.write(_TEST_SUBSCRIPTION_CONTENT)

_TEST_SUBSCRIPTION_CONTENT = """
<html>
  <body>
    <form method=POST action="/pubsub/add_subscription">
      <p>Subscription URL:
        <input name="feed" type="text">
        <input type="submit">
      </p>
    </form>
  </body>
</html>
"""
