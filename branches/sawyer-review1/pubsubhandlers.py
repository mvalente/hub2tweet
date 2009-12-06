"""Handlers for subscriptions."""

import os
import urllib
import urllib2
import xml.dom.minidom

from google.appengine.ext import webapp

import feeds
import twitterutil
import bitly

def _get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc

def _get_title_and_link(title, link):
  title = entry.getElementsByTagName('title')
  title_element = title.getElementsByTagName('title')
  title = _get_text(title_element)
  title_short = title_text[0:140 - (1+len(link)]
  link = feeds.get_self(entry)
  link_short = bitly.get_shortened_url(href)
  msg = "%s %s" % (title_short, href_short)
  return msg

class AddSubscriptionHandler(webapp.RequestHandler):
  
  def post(self):
    user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
    feed_url = self.request.get('feed')
    callback_url = 'http://%s/pubsub' % os.environ['HTTP_HOST']
    xml_doc = urllib2.urlopen(feed_url).read()
    hub_link = feeds.get_hub(xml_doc)
    self_link = feeds.get_self(xml_doc)
    params = {'hub.callback': callback_url, 'hub.mode': 'subscribe', 'hub.topic': self_link, 'hub.verify': 'async'}
    data = urllib.urlencode(params)
    urllib2.urlopen(hub_link, data)
    sub = models.TopicSubscription(user_id=user.user_id, topic=self_link)
    sub.put() 

class NewContentTestHandler(webapp.RequestHandler):
  
  #def post(self):
  #  TODO(nathan): Add later

  # TODO(nathan): remove this, make a POST
  def get(self):
    self.handle_atom_feed(open('feedstest.xml').read())

  def handle_atom_feed(self, atom):
    xml_doc = xml.dom.minidom.parseString(atom)
    key, secret = twitterutil.get_key_and_secret(91536090) # hard-code hub2tweet for now
    elements = xml_doc.getElementsByTagName('entry')
    for entry in elements:
      msg = _get_title_and_link(entry)
      twitterutil.set_status(msg, key, secret)
      self.response.out.write('sent tweet ' + msg)

  

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
