"""
:mod:`zsl.utils.xml_helper` -- xml helpers
==========================================

Helper functions for working with XML and ElementTree.
"""
from __future__ import unicode_literals
from future.utils import viewitems

import xml.etree.cElementTree as ET
import requests
from functools import reduce


class NotValidXmlException(Exception):
    """Exception raised on invalid xml"""
    # TODO try to use some build in exception #13299
    pass


def required_attributes(element, *attributes):
    """Check element for required attributes. Raise ``NotValidXmlException`` on error.

    :param element: ElementTree element
    :param attributes: list of attributes names to check
    :raises NotValidXmlException: if some argument is missing
    """
    if not reduce(lambda still_valid, param: still_valid and param in element.attrib, attributes, True):
        raise NotValidXmlException(msg_err_missing_attributes(element.tag, *attributes))


def required_elements(element, *children):
    """Check element (``xml.etree.ElementTree.Element``) for required children, defined as XPath. Raise
    ``NotValidXmlException`` on error.

    :param element: ElementTree element
    :param children: list of XPaths to check
    :raises NotValidXmlException: if some child is missing
    """
    for child in children:
        if element.find(child) is None:
            raise NotValidXmlException(msg_err_missing_children(element.tag, *children))


def required_items(element, children, attributes):
    """Check an xml element to include given attributes and children.

    :param element: ElementTree element
    :param children: list of XPaths to check
    :param attributes: list of attributes names to check
    :raises NotValidXmlException: if some argument is missing
    :raises NotValidXmlException: if some child is missing
    """
    required_elements(element, *children)
    required_attributes(element, *attributes)


def msg_err_missing_attributes(tag, *attributes):
    """Format message for missing attributes.

    :param tag: tag name
    :param attributes: list of attributes
    :return: message
    :rtype: str
    """
    return "Missing one or more required attributes (%s) in xml tag %s" % ('|'.join(attributes), tag)


def msg_err_missing_children(tag, *children):
    """Format message for missing children.

    :param tag: tag name
    :param children: list of children
    :return: message
    :rtype: str
    """
    return "Missing one or more required children (%s) in xml tag %s" % ('|'.join(children), tag)


def attrib_to_dict(element, *args, **kwargs):
    """For an ElementTree ``element`` extract specified attributes. If an attribute does not exists, its value will be
    ``None``.

    attrib_to_dict(element, 'attr_a', 'attr_b') -> {'attr_a': 'value', 'attr_a': 'value'}

    Mapping between xml attributes and dictionary keys is done with kwargs.
    attrib_to_dict(element, my_new_name = 'xml_atribute_name', ..)
    """
    if len(args) > 0:
        return {key: element.get(key) for key in args}

    if len(kwargs) > 0:
        return {new_key: element.get(old_key) for new_key, old_key in viewitems(kwargs)}

    return element.attrib


def get_xml_root(xml_path):
    """Load and parse an xml by given xml_path and return its root.

    :param xml_path: URL to a xml file
    :type xml_path: str
    :return: xml root
    """
    tree = ET.fromstring(requests.get(xml_path).content)
    return tree.getroot()


def element_to_int(element, attribute=None):
    """Convert ``element`` object to int. If attribute is not given, convert ``element.text``.

    :param element: ElementTree element
    :param attribute: attribute name
    :type attribute: str
    :returns: integer
    :rtype: int
    """
    if attribute is not None:
        return int(element.get(attribute))
    else:
        return int(element.text)


def create_el(name, text=None, attrib=None):
    """Create element with given attributes and set element.text property to given
    text value (if text is not None)

    :param name: element name
    :type name: str
    :param text: text node value
    :type text: str
    :param attrib: attributes
    :type attrib: dict
    :returns: xml element
    :rtype: Element
    """
    if attrib is None:
        attrib = {}

    el = ET.Element(name, attrib)
    if text is not None:
        el.text = text
    return el
