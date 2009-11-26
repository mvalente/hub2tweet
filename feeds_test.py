"""Tests for feeds utility."""

import unittest
import feeds


class FeedsTestCase(unittest.TestCase):

  def runTest(self):
    hub = feeds.get_hub_from_feed(open('feedstest.xml').read())

    # This should be the hub for the given feed.
    self.assertEqual(hub, 'http://pubsubhubbub.appspot.com/')


if __name__ == '__main__':
    unittest.main()
