"""Handlers for subscriptions."""

import os

import twitterutil

from google.appengine.ext import webapp

import urllib2

import urllib

import feeds

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
