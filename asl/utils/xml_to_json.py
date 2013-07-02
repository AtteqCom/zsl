class XmlToJsonException(Exception):
    pass

class NotCompleteXmlException(Exception):
    pass

def xml_to_json(element, definition, required=False):
    
    # handle simple definition
    if isinstance(definition, str) and len(definition) > 0:
        if definition[0] == '@': # test for attribute
            return element.get(definition[1:])
        
        # get tag text
        else:
            sub_element = element.find(definition)
            
            if sub_element is None:
                if required:
                    raise NotCompleteXmlException('Expecting {0} in element {1}'.format(definition, element.tag))
                return None
            
            return sub_element.text.strip() if sub_element.text else None        
    
    # handle tuple                
    elif isinstance(definition, tuple):
        return  _parse_tuple(element, definition, required)
    
    # handle dict
    elif isinstance(definition, dict):
        return _parse_dict(element, definition)
    
    # handle list
    elif isinstance(definition, list):
        return _parse_list(element, definition)
    
    elif hasattr(definition, '__call__'):
        return definition(element)
    
    # default
    else:
        return element.text.strip() if element.text else None  

def _parse_dict(element, definition):
    sub_dict = {}
        
    for name, subdef in definition.items():
        (name, required) = _parse_name(name)
        
        sub_dict[name] = xml_to_json(element, subdef, required)
    
    return sub_dict

def _parse_tuple(element, definition, required):
    d_len = len(definition)

    if d_len == 0:
        return None
    if d_len == 1:
        return xml_to_json(element, definition[0], required)
    
    first = definition[0]
    
    if hasattr(first, '__call__'):
        return first(*map(lambda d: xml_to_json(element, d), definition[1:]))
        
    if not isinstance(first, str):
        raise XmlToJsonException('Tuple definition must start with function or string')
    
    if first[0] == '@':
        raise XmlToJsonException('Tuple definition must not start with attribute')
    
    sub_elem = element.find(first)
    
    if sub_elem is None:
        if required:
            raise NotCompleteXmlException('Expecting {0} in element {1}'.format(first, element.tag))
        
        return None
    
    return xml_to_json(sub_elem, definition[1], required)             

def _parse_list(element, definition):
    if len(definition) == 0:
        raise XmlToJsonException('List definition needs some definition')

    tag = definition[0]
    tag_def = definition[1] if len(definition) > 1 else None

    sub_list = []
   
    for el in element.findall(tag):
        sub_list.append(xml_to_json(el, tag_def))
        
    return sub_list

def _parse_name(name):
    required = False
    
    if name[-1] == '*':
        name = name[0:-1]
        required = True
    
    return (name, required)