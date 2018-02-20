"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Tests for the parser.
"""

from unittest import TestCase
# from django.test.testcases import TestCase

from .Grammar import ProductionRule, Grammar, DescriptionParser, TreeNode, print_tree


# class ProductionRuleTest(TestCase):
#     """
#     Test the various cases of rules we may encounter.
#     """
#
#     def test_rule_with_no_terminals_one_non(self):
#         """
#         Test a rule where a lh sym goes to one non term sym and no alternation.
#         """
#         # Start with a production rule with one non terminal
#         expected_terminals = [[None]]
#         expected_non_terminals = [['type_list']]
#
#         # Setup grammar rule
#         left = 'beer'
#         right = ['<type_list>']
#
#         # Instantiate production rule
#         rule = ProductionRule(left, right)
#
#         self.assertTrue(rule.left_hand is left)
#         self.assertEqual(len(rule.non_terminals), len(rule.terminals))
#         self.assertEqual(rule.non_terminals, expected_non_terminals)
#         self.assertEqual(rule.terminals, expected_terminals)
#
#     def test_rule_with_no_terminals_two_non(self):
#         """
#         Test a rule where a lh sym goes to a case with two non term sym with no alternation.
#         """
#         # Start with a production rule with one non terminal
#         expected_terminals = [[None, None]]
#         expected_non_terminals = [['type', 'type_list']]
#
#         # Setup grammar rule
#         left = 'type_list'
#         right = ['<type> <type_list>']
#
#         # Instantiate production rule
#         rule = ProductionRule(left, right)
#
#         self.assertTrue(rule.left_hand is left)
#         self.assertEqual(rule.non_terminals, expected_non_terminals)
#         self.assertEqual(rule.terminals, expected_terminals)
#
#     def test_rule_with_no_terminals_three_non(self):
#         """
#         Test a rule where a lh sym goes to a case with three non term sym with no alternation.
#         In the essence of strong induction, we will assume any more than non term syms will have similar results.
#         """
#         # Start with a production rule with one non terminal
#         expected_terminals = [[None, None, None]]
#         expected_non_terminals = [['type', 'sep', 'type_list']]
#
#         # Setup grammar rule
#         left = 'type_list'
#         right = ['<type> <sep> <type_list>']
#
#         # Instantiate production rule
#         rule = ProductionRule(left, right)
#
#         self.assertTrue(rule.left_hand is left)
#         self.assertEqual(rule.non_terminals, expected_non_terminals)
#         self.assertEqual(rule.terminals, expected_terminals)
#
#     def test_rule_with_no_terminals_and_alternate_cases(self):
#         """
#         Test a rule where a lh sym goes to more than one case.
#         """
#         # Start with a production rule with one non terminal
#         expected_terminals = [[None], [None]]
#         expected_non_terminals = [['ales'], ['stouts']]
#
#         # Setup grammar rule
#         left = 'adj_ale'
#         right = ['<ales>', '<stouts>']
#
#         # Instantiate production rule
#         rule = ProductionRule(left, right)
#
#         self.assertTrue(rule.left_hand is left)
#         self.assertEqual(rule.non_terminals, expected_non_terminals)
#         self.assertEqual(rule.terminals, expected_terminals)
#
#     def test_rule_with_no_terms_and_alternation_multi_non_terms(self):
#         """
#         Test a rule where a lh sym goes to more than one case and multiple non terms in rh cases.
#         """
#         # Start with a production rule with one non terminal
#         expected_terminals = [[None, None, None], [None, None], [None, None]]
#         expected_non_terminals = [['non_term0', 'non_term1', 'ales'], ['adj', 'stouts'], ['non_term2', 'non_term3']]
#
#         # Setup grammar rule
#         left = 'adj_ale'
#         right = ['<non_term0> <non_term1> <ales>', '<adj> <stouts>', '<non_term2> <non_term3>']
#
#         # Instantiate production rule
#         rule = ProductionRule(left, right)
#
#         self.assertTrue(rule.left_hand is left)
#         self.assertEqual(rule.non_terminals, expected_non_terminals)
#         self.assertEqual(rule.terminals, expected_terminals)
#
#     def test_rule_with_only_terms(self):
#         """
#         Test a rule whose rh is only terminal symbols.
#         """
#         expected_terminals = [['american'], ['brown']]
#         expected_non_terms = [[None], [None]]
#
#         # Setup grammar rule
#         left = 'adj'
#         right = ['american', 'brown']
#
#         rule = ProductionRule(left, right)
#
#         self.assertEqual(rule.left_hand, left)
#         self.assertEqual(rule.terminals, expected_terminals)
#         self.assertEqual(rule.non_terminals, expected_non_terms)
#
#         # Grammar should have a property for each non term that equals it's corresponding Production Rules
#         # from .Grammar import Grammar
#         self.assertTrue(rule is getattr(Grammar, 'brown'))
#         self.assertTrue(rule is getattr(Grammar, 'american'))
#
#         self.assertEqual(Grammar.non_terminals, right)


class TestParser(TestCase):

    def setUp(self):
        # Grammar.build()
        self.parser = DescriptionParser("I like india pale ales, brown lagers and stouts")

    def test_shift(self):

        stack = []
        self.parser.shift(stack, self.parser.tokens)
        self.assertEqual(stack, ['I'])
        self.assertEqual(self.parser.tokens, ['like', 'lagers', 'and', 'stouts'])

    def test_case_matches_stack_with_strings_only(self):
        # Arrange
        stack = ['lager']
        case = ['<adj_list>', 'lager']

        # Act
        result = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case)

    def test_case_matches_stack_with_non_terms_and_strings(self):
        # Arrange
        stack = [TreeNode('<adj_list>'), 'lager']
        case = ['<adj_list>', 'lager']

        # Act
        result = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case)

        # Arrange
        stack = [TreeNode('<type>'), TreeNode('<type_list>')]
        case = ['<type>', '<type_list>']

        # Act
        result = self.parser.case_matches_stack(case, stack)

        # Assert
        self.assertTrue(result is case, "%s %s" % (result, case))

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
