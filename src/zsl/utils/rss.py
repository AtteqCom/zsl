"""
:mod:`zsl.utils.rss`
--------------------

Helper function for handling rss.

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals
from future.utils import viewitems

import xml.etree.cElementTree as ET


def complex_el_from_dict(parent, data, key):
    """Create element from a dict definition and add it to ``parent``.

    :param parent: parent element
    :type parent: Element
    :param data: dictionary with elements definitions, it can be a simple \
    {element_name: 'element_value'} or complex \
    {element_name: {_attr: {name: value, name1: value1}, _text: 'text'}}
    :param key: element name and key in ``data``
    :return: created element
    """
    el = ET.SubElement(parent, key)
    value = data[key]

    if isinstance(value, dict):
        if '_attr' in value:
            for a_name, a_value in viewitems(value['_attr']):
                el.set(a_name, a_value)

        if '_text' in value:
            el.text = value['_text']

    else:
        el.text = value

    return el


def element_from_dict(parent, data, element):
    """Create ``element`` to ``parent`` and sets its value to data[element], which
    will be removed from the ``data``.

    :param parent: parent element
    :type parent: Element
    :param data: dictionary where data[element] is desired value
    :type data: dict(str, str)
    :param element: name of the new element
    :type element: str
    :return: created element
    """
    el = ET.SubElement(parent, element)
    el.text = data.pop(element)

    return el


def rss_create(channel, articles):
    """Create RSS xml feed.

    :param channel: channel info [title, link, description, language]
    :type channel: dict(str, str)
    :param articles: list of articles, an article is a dictionary with some \
    required fields [title, description, link] and any optional, which will \
    result to `<dict_key>dict_value</dict_key>`
    :type articles: list(dict(str,str))
    :return: root element
    :rtype: ElementTree.Element
    """
    channel = channel.copy()

    # TODO use deepcopy
    # list will not clone the dictionaries in the list and `elemen_from_dict`
    # pops items from them
    articles = list(articles)

    rss = ET.Element('rss')
    rss.set('version', '2.0')

    channel_node = ET.SubElement(rss, 'channel')

    element_from_dict(channel_node, channel, 'title')
    element_from_dict(channel_node, channel, 'link')
    element_from_dict(channel_node, channel, 'description')
    element_from_dict(channel_node, channel, 'language')

    for article in articles:
        item = ET.SubElement(channel_node, 'item')

        element_from_dict(item, article, 'title')
        element_from_dict(item, article, 'description')
        element_from_dict(item, article, 'link')

        for key in article:
            complex_el_from_dict(item, article, key)

    return ET.ElementTree(rss)
