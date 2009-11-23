"""Utilities for parsing Atom feeds."""

import xml.dom.minidom

def get_hub_from_feed(xml_doc):
  """If a feed has a <link rel='hub'> tag, return the href."""
  if type(xml_doc) is str:
    xml_doc = xml.dom.minidom.parseString(xml_doc)
  # At this point, xml_doc is a Document.
  elements = xml_doc.getElementsByTagName('link')
  for i in elements:
    if i.hasAttribute('rel'):
      if i.getAttribute('rel') == 'hub':
        href = i.getAttribute('href')
  return href
