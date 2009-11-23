"""Utilities for parsing Atom feeds."""

import xml.dom.minidom

def get_hub_from_feed(xml_doc):
  """If a feed has a <link rel='hub'> tag, return the href."""
  
  # If the parameter is a string, convert to a Document.
  if type(xml_doc) is str:
    xml_doc = xml.dom.minidom.parseString(xml_doc)
  elements = xml_doc.getElementsByTagName('link')
  for i in elements:
    if i.hasAttribute('rel')==True:
      if i.getAttribute('rel') == 'hub':
        href = i.getAttribute('href')
  return href
  # TODO(sawyer): Implement.
  # At this point, xml_doc is a Document.
  # See http://docs.python.org/library/xml.dom.html#document-objects
