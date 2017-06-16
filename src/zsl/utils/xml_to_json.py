"""
:mod:`zsl.utils.xml_to_json` -- xml helpers
-------------------------------------------

Helper functions for simpler parsing xml into object with schemas.
"""
from __future__ import unicode_literals
from future.utils import viewitems


class XmlToJsonException(Exception):
    """Exception raised during converting xml to json."""
    # TODO make use of build in exception, see bug #13299
    pass


class NotCompleteXmlException(Exception):
    """Exception raised during parsing an invalid XML."""
    # TODO make use of build in exception, see bug #13299
    pass


def xml_to_json(element, definition, required=False):
    # TODO document tuple - it looks little too complex
    """Convert XML (ElementTree) to dictionary from a definition schema.

    Definition schema can be a simple string - XPath or @attribute for
    direct extraction or a complex one described by

    * dictionary ``{key: 'xpath or @attribute', second: 'complex definition'}`` \
      required parameters can be marked with * at the end
    * list ``[xpath, [definition]]`` - create a list of all elements found by \
      xpath, parse the parts with given definition if provided as second \
      argument
    * Callable - parse the element by given function, can be handy as a part \
      of complex definition

    :param element: ElementTree element
    :type element: ElementTree.Element
    :param definition: schema for the json
    :type definition: Union[str, tuple, dict, list, Callable]
    :param required: parsed value should be not None
    :type required: bool
    :return: parsed xml
    :rtype: Union[dict, str, list]
    """
    # handle simple definition
    if isinstance(definition, str) and len(definition) > 0:
        if definition[0] == '@':  # test for attribute
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
        return _parse_tuple(element, definition, required)

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
    """Parse xml element by a definition given in dict format.

    :param element: ElementTree element
    :param definition: definition schema
    :type definition: dict
    :return: parsed xml
    :rtype: dict
    """
    sub_dict = {}

    for name, subdef in viewitems(definition):
        (name, required) = _parse_name(name)

        sub_dict[name] = xml_to_json(element, subdef, required)

    return sub_dict


def _parse_tuple(element, definition, required):
    """Parse xml element by a definition given in tuple format.

    :param element: ElementTree element
    :param definition: definition schema
    :type definition: tuple
    :param required: parsed value should be not None
    :type required: bool
    :return: parsed xml
    """
    # TODO needs to be documented properly.
    d_len = len(definition)

    if d_len == 0:
        return None
    if d_len == 1:
        return xml_to_json(element, definition[0], required)

    first = definition[0]

    if hasattr(first, '__call__'):
        # TODO I think it could be done without creating the array
        # first(xml_to_json(element, d) for d in definition[1:]) test it
        return first(*[xml_to_json(element, d) for d in definition[1:]])

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
    """Parse xml element by definition given by list.

    Find all elements matched by the string given as the first value
    in the list (as XPath or @attribute).

    If there is a second argument it will be handled as a definitions
    for the elements matched or the text when not.

    :param element: ElementTree element
    :param definition: definition schema
    :type definition: list
    :return: parsed xml
    :rtype: list
    """
    if len(definition) == 0:
        raise XmlToJsonException('List definition needs some definition')

    tag = definition[0]
    tag_def = definition[1] if len(definition) > 1 else None

    sub_list = []

    for el in element.findall(tag):
        sub_list.append(xml_to_json(el, tag_def))

    return sub_list


def _parse_name(name):
    """Parse name in complex dict definition.

    In complex definition required params can be marked with `*`.

    :param name:
    :return: name and required flag
    :rtype: tuple
    """
    required = False

    if name[-1] == '*':
        name = name[0:-1]
        required = True

    return name, required
