import unittest
import xml.etree.cElementTree

from zsl.utils.xml_to_json import xml_to_json


class TestXmlToJson(unittest.TestCase):
    xml = '''<?xml version="1.0"?>
<root atr="34">
    <simple id="hou"/>
    <node_a>
        text
    </node_a>
    
    <complex>
        <node_b>
            krajina
        </node_b>
        
        <node_c hud="klud"/>
    </complex>
    
    <node_d id="23"/>
    
    <list>
        <item prop="1">34</item>
        <item prop="0">35</item>
        <item prop="1">38</item>
        <item prop="0">39</item>
    </list>
</root>
    '''

    def setUp(self):
        self._root = xml.etree.cElementTree.fromstring(self.xml)

    def test_simple_definitions(self):
        def_attribute = '@atr'
        def_node = 'node_a'
        def_complex_node = 'complex/node_b'

        self.assertEqual("34", xml_to_json(self._root, def_attribute))
        self.assertEqual("text", xml_to_json(self._root, def_node))
        self.assertEqual("krajina", xml_to_json(self._root, def_complex_node))

    def test_func_callback(self):
        def func(element):
            return element.tag

        self.assertEquals('root', xml_to_json(self._root, func))

    def test_tuple_definitions(self):
        self.assertEqual('23', xml_to_json(self._root, ('node_d', '@id')))
        self.assertEqual('klud', xml_to_json(self._root, ('complex/node_c', '@hud')))
        self.assertEqual('textkrajina', xml_to_json(self._root, (lambda x, y: x + y, 'node_a', 'complex/node_b')))

    def test_list_definitions(self):
        self.assertListEqual(['34', '35', '38', '39'], xml_to_json(self._root, ['list/item']))
        self.assertListEqual(['1', '0', '1', '0'], xml_to_json(self._root, ['list/item', '@prop']))

    def test_dict_definitions(self):
        definition = {
            'id': '@atr',
            'a': 'node_a',
            'b': ('node_d', '@id'),
            'c': 'complex/node_b'
        }

        expected = {'id': '34', 'a': 'text', 'b': '23', 'c': 'krajina'}

        self.assertDictEqual(expected, xml_to_json(self._root, definition))


if __name__ == "main":
    unittest.main()
