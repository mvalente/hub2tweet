"""Tests for feeds utility."""

import unittest
import feeds


class FeedsTestCase(unittest.TestCase):

  def testHub(self):
    hub = feeds.get_hub_from_feed(open('feedstest.xml').read())

    # This should be the hub for the given feed.
    self.assertEqual(hub, 'http://pubsubhubbub.appspot.com/')

  def testSelf(self):
    self_href = feeds.get_self_from_feed(open('feedstest.xml').read())

    # This should be the hub for the given feed.
    self.assertEqual(self_href, 'http://feeds.feedburner.com/blogspot/MKuf')

if __name__ == '__main__':
    unittest.main()
