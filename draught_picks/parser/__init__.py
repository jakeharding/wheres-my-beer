"""
__init__.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  J.Harding

Beer description parser.
"""
#
# import re
# from collections import OrderedDict

# from .Grammar import Grammar

# Grammar.build()

# from .NonTerminal import NonTerminal, LeftHandNonTerminal, RightHandNonTerminal
#
#
# comment_re = re.compile(r'^#.*|\s+')  # Whole line comments in the grammar file will be ignored.
#
# with open('parser/grammar') as fl:
#     for line in fl.readlines():
#         if comment_re.match(line):
#             "Skip any comments or whitespace lines"
#             continue
#         # Find all Non terminals and create objects
#
#         # print(LeftHandNonTerminal.regex.match(line).group('symbol'))
#         # print(RightHandNonTerminal.regex.findall(line))
#         print(line)
#         ln = line.split('::=')[1].split('|')
#         print(ln)
        # for m in RightHandNonTerminal.regex.finditer(ln):
        #     print(m.string)


# class Grammar(object):
#     """
#     Holds the grammar for parsing the description.
#     """
#     # Avoid right hand production or case containing more than one terminal: '<term1> nonterm1 nonterm2'
#     # Create another production rule instead.
#     grammar = OrderedDict({
#         'beer': ['<type_list>'],
#         'type_list': ['<type> <sep> <type_list>', '<epsilon>'],
#         'type': ['<adj_ale>', '<lager>'],
#         'adj_ale': ['<ales>', '<stouts>'],
#         'ales': ['<adj_list> ale', '<adj_list> ales', ],
#         'stouts': ['<adj_list> stout', '<adj_list> stouts'],
#         'lager': ['<adj_list> lager', '<adj_list> lagers'],
#         'adj_list': ['<adj> <sep> <adj_list>', '<epsilon>'],
#         'adj': ['<color>', '<origin>'],
#         'color': ['pale', 'brown'],
#         'origin': ['india', 'american'],
#         'sep': ['-', ',', 'and', '<epsilon>'],
#         'epsilon': [''],
#     })
#
#     description = ''
#     rules = []
#
#     def __init__(self, description):
#         self.description = description
#         # self.rules = []
#
#     @staticmethod
#     def build():
#         rules = []
#         for lh, rh in Grammar.grammar.items():
#             rules.append(ProductionRule(lh, rh))
#         setattr(Grammar, 'rules', rules)


# class ProductionRule(object):
#     """
#     Class to model a production rule in the grammar.
#     Right hand side could possibly have non terminal, terminals, or combination of both.
#
#     """
#     sym_regex = re.compile(r'^<(?P<symbol>\w+)>$')
#     left_hand = ''  # Left hand side of the grammar. Will match the key of Grammar.grammar
#
#     # 2D lists are used to map the non terminals to terminal in the same case of a right hand rule.
#     # For instance, rh = ['<non_term0> <non_term0.1>', '<non_term0> term1', '<non_term1> term2 term3'] would map to
#     # terminals = [['non_term0', non_term0.1'], ['non_term0'], ['non_term1']]
#     # non_terminals =[['', ''], ['term1'],  ['term2', 'term3']]
#     # The indices of the terminals will relate to the indices of the non terminals of the lengths will match.
#     terminals = []  # A 2D list of terminals from right hand side.
#     non_terminals = []  # A 2D list is used to map non terminals from right hand side.
#
#     def __init__(self, lh, rh):
#         # Reset the list to empty or they will be held statically in memory
#         self.terminals = []
#         self.non_terminals = []
#         self.left_hand = lh
#         # Iterate over the value of this rule in the grammar map. This at least one terminal or non terminal.
#         for r in rh:
#             rh_case = r.split()  # Split on whitespace to get a list of tokens in a case of this right hand rule
#             this_case_terms = [None] * len(rh_case)  # List won't be longer than the # of tokens in the production rule
#             this_case_non_terms = [None] * len(rh_case)
#             for (i, n) in enumerate(rh_case):
#                 has_non_term = False  # Flag to tell if a term symbol is associated with a non term
#                 m = self.sym_regex.match(n)
#                 # curr_index = len(this_case_non_terms)
#                 if m:
#                     "We have a symbol to use on the left hand side of the grammar"
#                     this_case_terms[i] = m.group('symbol')
#                     this_case_non_terms[i] = None
#                     has_non_term = True
#                     # this_case_non_terms.append('')  # Append an empty string to maintain consistent length
#                 else:
#                     "We have a terminal symbol associated with a non terminal."
#                     # All rules (so far) are left recursive, ie 'adj_list ales' so we have to set the previous index
#                     # to the term sym if it is associated with a non term sym.
#                     term_index = i
#                     if has_non_term:
#                         term_index -= 1
#                     this_case_non_terms[term_index] = n
#
#                     # Get the existing property on the grammar or an empty set if it doesn't exist
#                     g_rules = getattr(Grammar, n, set())
#
#                     # Set property on Grammar class of non term the set containing this rule
#                     # We access the production rule for a non term when parsing a description by
#                     # getattr(Grammar, non_term). Will return None if it doesn't exist
#                     # Python set.add method has O(1) time complexity
#                     # according to https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
#                     setattr(Grammar, n, g_rules.add(self))
#
#             self.terminals.append(this_case_terms)
#             self.non_terminals.append(this_case_non_terms)
#             # print(self.rule_regex.findall(i))
#             # for r in self.rule_regex.findall(i):
#             #     print(r)
#         print(self.terminals)
#         print(self.non_terminals)
#         print('\n')


# class TreeNode(object):
#     production_rule = None
#     children = []
#     str_value = ''


# __all__ = ['ProductionRule', 'Grammar']
# Grammar.build()
# print(Grammar.__dict__)
