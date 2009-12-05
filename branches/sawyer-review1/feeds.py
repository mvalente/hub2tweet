"""Utilities for parsing Atom feeds."""

import xml.dom.minidom

def get_hub(xml_doc):
  """If a feed has a <link rel='hub'> tag, returns the href."""
  return _get_href_from_feed(xml_doc, 'hub')

def get_self(xml_doc):
  """If a feed has a <link rel='self'> tag, return the href."""
  return _get_href_from_feed(xml_doc, 'self')
  
def _get_href_from_feed(xml_doc, rel_type):
  """If a feed has a <link rel='hub'> or <link rel='self'> tag, returns the href"""
  if type(xml_doc) is str:
    xml_doc = xml.dom.minidom.parseString(xml_doc)
  # At this point, xml_doc is a Document.
  elements = xml_doc.getElementsByTagName('link')
  for i in elements:
    if i.hasAttribute('rel'):
      if i.getAttribute('rel') == rel_type:
        href = i.getAttribute('href')
  return href
