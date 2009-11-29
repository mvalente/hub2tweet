"""Handlers for subscriptions."""

import os

import twitterutil

from google.appengine.ext import webapp

class AddSubscriptionHandler(webapp.RequestHandler):
  
  def post(self):
    user = twitterutil.get_user_by_token_key(self.request.cookies['token'])
    feed_url = self.request.get('feed')
    callback_url = 'http://%s/pubsub' % os.environ['HTTP_HOST']

    # TODO(sawyer): You need to do the following:
    # 1. Fetch the feed.
    # 2. Get the hub and the self links
    # 3. Use urllib2 to send a POST request to the hub to subscribe to the feed
    # in 'self'.
    # See http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.2.html#anchor5
    # Your parameters should be hub.callback (above), hub.mode ('subscribe'),
    # hub.topic (value of self link), hub.verify ('async' for now... I'll handle
    # the rest later.
    # 4. Make a new models.TopicSubscription with user.user_id for a user_id and
    # the self href as the topic.

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
