#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys, os
    here_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
    sys.path.append(here_dir)

import unittest

from jquery_unparam import parse_key_pair
from jquery_unparam import merge_two_structs
from jquery_unparam import jquery_unparam_unquoted

class TestJqueryUnparamParseKeyPair(unittest.TestCase):
    def test_parse_key_pair_simple(self):
        self.assertEqual(
            parse_key_pair('a=1'),
            {'a': '1'})

    def test_parse_key_pair_list(self):
        self.assertEqual(
            parse_key_pair('a[]=1'),
            {'a': ['1']})

    def test_parse_key_pair_dict(self):
        self.assertEqual(
            parse_key_pair('a[b]=1'),
            {'a': {'b': '1'}})

    def test_parse_key_pair_dict_in_list(self):
        self.assertEqual(
            parse_key_pair('a[][a]=1'),
            {'a': [{'a': '1'}]})

    def test_parse_key_pair_list_in_dict(self):
        self.assertEqual(
            parse_key_pair('a[b][]=1'),
            {'a': {'b': ['1']}})

class TestJqueryUnparamMergeTwoStructs(unittest.TestCase):
    def test_merge_two_structs_simple(self):
        self.assertEqual(
            merge_two_structs('1', '2'),
            '2')

    def test_merge_two_structs_lists(self):
        self.assertEqual(
            merge_two_structs(['1'], ['2']),
            ['1', '2'])

    def test_merge_two_structs_lists_in_dict(self):
        self.assertEqual(
            merge_two_structs({'a': ['b']}, {'a': ['c']}),
            {'a': ['b', 'c']})

    def test_merge_two_structs_dicts_differentkeys(self):
        self.assertEqual(
            merge_two_structs({'a': '1'}, {'b': '2'}),
            {'a': '1', 'b': '2'})
    
    def test_merge_two_structs_dicts_samekeys(self):
        self.assertEqual(
            merge_two_structs({'a': '1'}, {'a': '2'}),
            {'a': '2'})

    def test_merge_two_structs_complex(self):
        self.assertEqual(
            merge_two_structs({'a': {'b': {'c': ['d', 'e', {'f': 'g'}]}}}, {'a': {'b': {'c': ['h', 'i']}}}),
            {'a': {'b': {'c': ['d', 'e', {'f': 'g'}, 'h', 'i']}}})

class TestJqueryUnparam(unittest.TestCase):
    def test_jquery_unparam_unquoted_simple(self):
        self.assertEqual(
            jquery_unparam_unquoted("a=b"),
            {'a': 'b'}
            )
        
    def test_jquery_unparam_unquoted_list(self):
        self.assertEqual(
            jquery_unparam_unquoted("a[]=b&a[]=c"),
            {'a': ['b', 'c']}
            )

    def test_jquery_unparam_unquoted_twice(self):
        self.assertEqual(
            jquery_unparam_unquoted("a=a&a=b"),
            {'a': 'b'}
            )
    
    def test_jquery_unparam_unquoted_obj(self):
        self.assertEqual(
            jquery_unparam_unquoted("a[b]=c"),
            {'a': {'b': 'c'}}
            )
    
    def test_jquery_unparam_unquoted_list_in_obj(self):
        self.assertEqual(
            jquery_unparam_unquoted("a[b][]=c&a[b][]=d"),
            {'a': {'b': ['c', 'd']}}
            )
    
    def test_jquery_unparam_unquoted_list_in_obj2(self):
        self.assertEqual(
            jquery_unparam_unquoted("a[b][]=c&a[b][]=d&a[e]=321"),
            {'a': {'b': ['c', 'd'], 'e': '321'}}
            )
    
    def test_jquery_unparam_unquoted_more_complex(self):
        self.assertEqual(
            jquery_unparam_unquoted("a[b][]=c&a[b][]=d&a[e][2][e][]=f&a[e][2][e][]=h_i"),
            {'a': {'b': ['c', 'd'], 'e': {'2': {'e': ['f', 'h_i']}}}}
            )
    
    def test_jquery_unparam_unquoted_novalue(self):
        self.assertEqual(
            jquery_unparam_unquoted("a"),
            {'a': ''}
            )
    
    def test_jquery_unparam_unquoted_novalue_and_equal(self):
        self.assertEqual(
            jquery_unparam_unquoted("a=&b"),
            {'a': '', 'b': ''}
            )

    def test_jquery_unparam_unquoted_nokey(self):
        self.assertEqual(
            jquery_unparam_unquoted("=b"),
            {}
            )
        
    def test_jquery_unparam_unquoted_unicode(self):
        self.assertEqual(
            jquery_unparam_unquoted(u"a=ыыы"),
            {'a': u'ыыы'}
            )
        
if __name__ == '__main__':
    unittest.main()
