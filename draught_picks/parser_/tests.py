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
        # self.parser_ = DescriptionParser("""Our first beer has been aptly named ""633"" after the Regions telephone exchange for starters.  ""If I could call a beer home, this would be the one."" ~ Win

# It is a mildly hoppy pale ale using a 2 row, vienna, and munich malts for body,color, and head retention. It is hopped with American west coast hops later in the boil giving it a nice citrus hop flavor and very mild aroma. Slight addition of a roasted caramel malt gives ""633"" it's signature 'sunset over the harbor glow'.""")

    def test_shift(self):

        stack = []
        self.parser.shift(stack, self.parser.tokens)
        self.assertEqual(stack, [''])
        self.assertEqual(self.parser.tokens, ['like', 'india', 'pale', 'ales', 'brown', 'lagers', 'and', 'dark', 'stouts'])

    def test_init(self):
        a_parser = DescriptionParser("American-style lagers and ales")

        self.assertEqual(a_parser.description, "american style lagers and ales")
        self.assertEqual(a_parser.tokens, ["american", "style", "lagers", "and", "ales"])

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

    def test_reduce(self):
        # Arrange
        stack = ["lagers"]

        # Act
        self.parser.reduce(stack, 1)

        # Assert it should parse the right most symbol to a tree
        self.assertTrue(isinstance(stack[0], TreeNode) and stack[0].name == "<lager>", stack[0].name)
        stack.append("stouts")
        self.parser.reduce(stack, 0)
        self.assertTrue(isinstance(stack[1], TreeNode) and stack[1].name == "<stouts>", stack[1].name)

    def test_parse(self):
        self.parser.parse()
