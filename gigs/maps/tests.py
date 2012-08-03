import mock

from django.utils import unittest
from django import template
from gigs.maps.templatetags import maps

class TagsTestCase(unittest.TestCase):
    fixtures = ['map_test_data.json']
    output_node_class = template.Node

    def setUp(self):
        pass

class DoMapTestCase(TagsTestCase):
    output_node_class = maps.MapNode

    def test_map_tag_dispatch(self):
        token = template.Token(template.TOKEN_TEXT, "map test_variable")
        parser = mock.Mock()
        node = maps.do_map(parser, token)
        self.assertEqual(node.__class__, maps.MapNode)
    
    def test_search_map_tag_dispatch(self):
        token = template.Token(template.TOKEN_TEXT, "search_map test_variable")
        parser = mock.Mock()
        node = maps.do_map(parser, token)
        self.assertEqual(node.__class__, maps.GigSearchMapNode)
    
    def test_incorrect_tag_name(self):
        token = template.Token(template.TOKEN_TEXT, "nap test_variable")
        parser = mock.Mock()
        node = maps.do_map(parser, token)
        self.assertEqual(node.__class__, self.output_node_class)

    def test_incorrect_params(self):
        token_strings = ["map test_variable and_then_some", "map"]
        parser = mock.Mock()
        for token_string in token_strings:
            token = template.Token(template.TOKEN_TEXT, token_string)
            self.assertRaises(template.TemplateSyntaxError, maps.do_map, parser, token)

