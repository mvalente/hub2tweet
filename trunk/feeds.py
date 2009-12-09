"""Utilities for parsing Atom feeds."""

import xml.dom
import xml.dom.minidom


def get_hub(node):
  """If a feed has a <link rel='hub'> tag, returns the href."""
  return _get_href_from_feed(node, 'hub')

def get_self(node):
  """If a feed has a <link rel='self'> tag, return the href."""
  return _get_href_from_feed(node, 'self')
  
def _is_element_or_document(node):
  return node.nodeType in [xml.dom.Node.DOCUMENT_NODE, xml.dom.Node.ELEMENT_NODE]

def _get_href_from_feed(node, rel_type):
  """If a feed has a <link rel='hub'> or <link rel='self'> tag, returns the href"""
  if type(node) is str:
    node = xml.dom.minidom.parseString(node)
    
  child_elements = filter(_is_element_or_document, node.childNodes)
  for element in child_elements:
    if element.tagName == 'link':
      if element.hasAttribute('rel'):
        if element.getAttribute('rel') == rel_type:
          return element.getAttribute('href')
