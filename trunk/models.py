from google.appengine.ext import db

"""Data models for hub2tweet."""


# Note on OAuthConfig:
#
# The configuration is stored in datastore as we don't want to check our
# private keys into an open source project.  The first config in the
# datastore will be used.  To set your config, go to the Interactive Console:
#
# http://localhost:8080/_ah/admin/interactive
#
# And add a config to the datastore manually (copy paste this code, and fill in
# the right key and secret).  You can verify and change with the Datastore
# Viewer.
"""
import models

config = models.OAuthConfig(
 consumer_key="<key>"
 consumer_secret="<secret>")

config.put()
"""


class OAuthConfig(db.Model):
  """OAuth configuration"""

  consumer_key = db.StringProperty(required=True)
  consumer_secret = db.StringProperty(required=True)

