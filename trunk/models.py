from google.appengine.ext import db

"""Data models for hub2tweet."""


# Note on OAuthConfig:
#
# The configuration is stored in datastore as we don't want to check our
# private keys into an open source project.  The first config in the
# datastore will be used.
#
# To help make this easier to set, a simple admin config page was added.
# On your server, visit: http://<server>/admin/oauth_config
#
# And add a config to the datastore manually (copy paste this code, and fill in
# the right key and secret).  You can verify and change with the Datastore
# Viewer.


class OAuthConfig(db.Model):
  """OAuth configuration"""

  consumer_key = db.StringProperty(required=True)
  consumer_secret = db.StringProperty(required=True)


class OAuthToken(db.Model):
  # key name is token
  secret = db.StringProperty(required=True)


class TwitterUser(db.Model):
  # key name is token
  secret = db.StringProperty(required=True)
  user_id = db.IntegerProperty(required=True)
  screen_name = db.StringProperty(required=True)
