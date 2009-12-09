"""Tests for feeds utility."""

import unittest
import feeds

import xml.dom.minidom


class FeedsTestCase(unittest.TestCase):

  def testHub(self):
    feed = xml.dom.minidom.parseString(open('feedstest.xml').read())
    hub = feeds.get_hub(feed.getElementsByTagName('feed')[0])

    # This should be the hub for the given feed.
    self.assertEqual(hub, 'http://pubsubhubbub.appspot.com/')

  def testSelf(self):
    feed = xml.dom.minidom.parseString(open('feedstest.xml').read())
    self_href = feeds.get_self(feed.getElementsByTagName('feed')[0])

    # This should be the hub for the given feed.
    self.assertEqual(self_href, 'http://feeds.feedburner.com/blogspot/MKuf')

if __name__ == '__main__':
    unittest.main()
