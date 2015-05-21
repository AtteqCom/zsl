'''
:mod:`asl.utils.rss`

.. moduleauthor:: Peter Morihladko
'''

import xml.etree.cElementTree as ET

def complex_el_from_dict(parent, data, key):
    el = ET.SubElement(parent, key)
    value = data[key]
    
    if isinstance(value, dict):
        if '_attr' in value:
            for a_name, a_value in value['_attr'].items():
                el.set(a_name, a_value)
        
        if '_text' in value:
            el.text = value['_text']
            
    else:
        el.text = value
        
    return el

def element_from_dict(parent, data, element):
    """
    Vytvori element z ``data``, tak, ze text bude hodnota v data + dany kluc vyhodi z data
    """
    el = ET.SubElement(parent, element)
    el.text = data.pop(element)
    
    return el

def rss_create(channel, articles):
    channel = channel.copy()
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
        
        for key in article.keys():
            complex_el_from_dict(item, article, key)
        
    return ET.ElementTree(rss)
