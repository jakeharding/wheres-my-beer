"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Tests for the parser.
"""

from django.test import TestCase

from .Grammar import DescriptionParser, TreeNode


class TestParser(TestCase):

    def setUp(self):
        self.parser = DescriptionParser("I like india pale ales, brown lagers and dark stouts")

    def test_shift(self):

        stack = []
        self.parser.shift(stack, self.parser.tokens)
        self.assertEqual(stack, [''])
        self.assertEqual(self.parser.tokens, ['like', 'india', 'pale', 'ales', 'brown', 'lagers', 'and', 'dark', 'stouts'])

    def test_case_matches_stack_with_strings_only(self):
        # Arrange
        stack = ['lager']
        case = ['<adj_list>', 'lager']

        # Act
        result, match = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case)
        self.assertEqual(match, 1)

    def test_case_matches_stack_with_non_terms_and_strings(self):
        # Arrange
        stack = [TreeNode('<adj_list>'), 'lager']
        case = ['<adj_list>', 'lager']

        # Act
        (result, match) = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case, result)
        self.assertEqual(match, 1)

        # Arrange
        stack = [TreeNode('<type>'), TreeNode('<type_list>')]
        case = ['<type>', '<type_list>']

        # Act
        result, match = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case, "%s %s" % (result, case))
        self.assertEqual(match, 2)

    # def test_reduce(self):
    #     # Arrange
    #     stack = ["lagers", "stouts"]
    #
    #     # Act
    #     result = self.parser.reduce(stack)

        # Assert
        # print(result[0].name, result[0].children)
        # print_tree(result[0])

    def test_parse(self):
        self.parser.parse()
