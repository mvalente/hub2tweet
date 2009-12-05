"""Handlers for subscriptions."""

import os
import urllib
import urllib2
import xml.dom.minidom

from google.appengine.ext import webapp

import feeds
import twitterutil

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

    # TODO(sawyer): Remove this.
    self.response.out.write(atom)

    # TODO(sawyer):
    # Loop through each <entry> tag in xml_doc.  (get elements by tag name)  From each,
    # get the value of the title tag and the href from the self tag.  Get the short form
    # of the href URL from bit.ly.  Then concatenate the title and short url to make something
    # that looks like "<title> <bitly URL>" -- cut off title so that it's no more than
    # 140 characters.  Then, post that message to Twitter with the below statement.

    # twitterutil.set_status(msg, key, secret)
    

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
