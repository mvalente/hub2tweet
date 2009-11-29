"""Utility methods for OAuth."""

from third_party import oauth

import models

def get_consumer():
  """Get an OAuth consumer object seeded by the datastore values."""
  auth_tuple = _get_consumer_key_and_secret()
  if auth_tuple:
    key, secret = auth_tuple
    return oauth.OAuthConsumer(key, secret)


def _get_consumer_key_and_secret():
  """Pull the key and secret from datastore."""
  configs = models.OAuthConfig.all()

  if configs.count():
    config = configs[0]
    return config.consumer_key, config.consumer_secret
