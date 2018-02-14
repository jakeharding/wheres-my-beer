"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Tests for the parser.
"""

from unittest import TestCase

from .Grammar import ProductionRule


class ProductionRuleTest(TestCase):
    """
    Test the various cases of rules we may encounter.
    """

    def test_rule_with_no_terminals_one_non(self):
        """
        Test a rule where a lh sym goes to one non term sym and no alternation.
        """
        # Start with a production rule with one non terminal
        expected_terminals = [[None]]
        expected_non_terminals = [['type_list']]

        # Setup grammar rule
        left = 'beer'
        right = ['<type_list>']

        # Instantiate production rule
        rule = ProductionRule(left, right)

        self.assertTrue(rule.left_hand is left)
        self.assertEqual(len(rule.non_terminals), len(rule.terminals))
        self.assertEqual(rule.non_terminals, expected_non_terminals)
        self.assertEqual(rule.terminals, expected_terminals)

    def test_rule_with_no_terminals_two_non(self):
        """
        Test a rule where a lh sym goes to a case with two non term sym with no alternation.
        """
        # Start with a production rule with one non terminal
        expected_terminals = [[None, None]]
        expected_non_terminals = [['type', 'type_list']]

        # Setup grammar rule
        left = 'type_list'
        right = ['<type> <type_list>']

        # Instantiate production rule
        rule = ProductionRule(left, right)

        self.assertTrue(rule.left_hand is left)
        self.assertEqual(rule.non_terminals, expected_non_terminals)
        self.assertEqual(rule.terminals, expected_terminals)

    def test_rule_with_no_terminals_three_non(self):
        """
        Test a rule where a lh sym goes to a case with three non term sym with no alternation.
        In the essence of strong induction, we will assume any more than non term syms will have similar results.
        """
        # Start with a production rule with one non terminal
        expected_terminals = [[None, None, None]]
        expected_non_terminals = [['type', 'sep', 'type_list']]

        # Setup grammar rule
        left = 'type_list'
        right = ['<type> <sep> <type_list>']

        # Instantiate production rule
        rule = ProductionRule(left, right)

        self.assertTrue(rule.left_hand is left)
        self.assertEqual(rule.non_terminals, expected_non_terminals)
        self.assertEqual(rule.terminals, expected_terminals)

    def test_rule_with_no_terminals_and_alternate_cases(self):
        """
        Test a rule where a lh sym goes to more than one case.
        """
        # Start with a production rule with one non terminal
        expected_terminals = [[None], [None]]
        expected_non_terminals = [['ales'], ['stouts']]

        # Setup grammar rule
        left = 'adj_ale'
        right = ['<ales>', '<stouts>']

        # Instantiate production rule
        rule = ProductionRule(left, right)

        self.assertTrue(rule.left_hand is left)
        self.assertEqual(rule.non_terminals, expected_non_terminals)
        self.assertEqual(rule.terminals, expected_terminals)

    def test_rule_with_no_terms_and_alternation_multi_non_terms(self):
        """
        Test a rule where a lh sym goes to more than one case and multiple non terms in rh cases.
        """
        # Start with a production rule with one non terminal
        expected_terminals = [[None, None, None], [None, None], [None, None]]
        expected_non_terminals = [['non_term0', 'non_term1', 'ales'], ['adj', 'stouts'], ['non_term2', 'non_term3']]

        # Setup grammar rule
        left = 'adj_ale'
        right = ['<non_term0> <non_term1> <ales>', '<adj> <stouts>', '<non_term2> <non_term3>']

        # Instantiate production rule
        rule = ProductionRule(left, right)

        self.assertTrue(rule.left_hand is left)
        self.assertEqual(rule.non_terminals, expected_non_terminals)
        self.assertEqual(rule.terminals, expected_terminals)

    def test_rule_with_only_terms(self):
        """
        Test a rule whose rh is only terminal symbols.
        """
        expected_terminals = [['american'], ['brown']]
        expected_non_terms = [[None], [None]]

        # Setup grammar rule
        left = 'adj'
        right = ['american', 'brown']

        rule = ProductionRule(left, right)

        self.assertEqual(rule.left_hand, left)
        self.assertEqual(rule.terminals, expected_terminals)
        self.assertEqual(rule.non_terminals, expected_non_terms)
