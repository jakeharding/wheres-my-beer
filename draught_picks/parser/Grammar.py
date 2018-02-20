"""
Grammar.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Define how a grammar and it's productions rules behave.
"""

import re, string
from collections import OrderedDict


class TreeNode(object):
    children = []
    name = ''

    def __init__(self, name, children=[]):
        self.name = name
        self.children = children


class ProductionRule(object):
    """
    Class to model a production rule in the grammar.
    Right hand side could possibly have non terminal, terminals, or combination of both.
    """
    sym_regex = re.compile(r'^(?P<symbol><\w+>)$')
    left_hand = ''  # Left hand side of the grammar. Will match a key in Grammar.grammar

    # 2D lists are used to map the non terminals to terminal in the same case of a right hand rule.
    # For instance, rh = ['<non_term0> <non_term0.1>', '<non_term0> term1', '<non_term1> term2 term3'] would map to
    # terminals = [['non_term0', non_term0.1'], ['non_term0'], ['non_term1']]
    # non_terminals =[['', ''], ['term1'],  ['term2', 'term3']]
    # The indices of the terminals will relate to the indices of the non terminals of the lengths will match.
    terminals = []  # A 2D list of terminals from right hand side.
    non_terminals = []  # A 2D list is used to map non terminals from right hand side.

    def __init__(self, lh, rh):
        # Reset the lists to empty or they will be held statically in memory
        # 2D lists. each member list is a case in the RH production of a grammar rule
        self.terminals = []
        self.non_terminals = []
        self.left_hand = lh
        # Iterate over the value of this rule in the grammar map. This at least one terminal or non terminal.
        for r in rh:
            rh_case = r.split()  # Split on whitespace to get a list of tokens in a case of this right hand rule
            this_case_terms = [None] * len(rh_case)  # List won't be longer than the # of tokens in the production rule
            this_case_non_terms = [None] * len(rh_case)
            for (i, n) in enumerate(rh_case):
                has_non_term = False  # Flag to tell if a term symbol is associated with a non term
                m = self.sym_regex.match(n)
                if m:
                    "We have a symbol to use on the left hand side of the grammar"
                    # this_case_terms[i] = None
                    this_case_non_terms[i] = m.group('symbol')
                    has_non_term = True
                    # this_case_non_terms.append('')  # Append an empty string to maintain consistent length
                else:
                    "We have a terminal symbol associated with a non terminal."
                    # All rules (so far) are left recursive, ie 'adj_list ales' so we have to set the previous index
                    # to the term sym if it is associated with a non term sym.
                    term_index = i
                    if has_non_term:
                        term_index -= 1
                    this_case_terms[term_index] = n

                    # Set property on Grammar class of non term the set containing this rule
                    # We access the production rule for a non term when parsing a description by
                    # getattr(Grammar, non_term). Will return None if it doesn't exist
                    # Python set.add method has O(1) time complexity
                    # according to https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
                    setattr(Grammar, n, self)

            self.terminals.append(this_case_terms)
            self.non_terminals.append(this_case_non_terms)
            # print(self.rule_regex.findall(i))
            # for r in self.rule_regex.findall(i):
            #     print(r)
        # print(self.left_hand)
        # print(self.terminals)
        # print(self.non_terminals)
        # print('\n')


class Grammar(object):
    """
    Holds the grammar for parsing the description.
    """
    # Avoid right hand production or case containing more than one terminal: '<term1> nonterm1 nonterm2'
    # Create another production rule instead.
    grammar = OrderedDict({
        '<beer>': ['<type_list>'],
        '<type_list>': ['<type> <type_list>', '<type> <type>'],
        '<type>': ['<ales>', '<lager>', '<adj_list> <type>'],
        # '<adj_ale>': ['<ales>', '<stouts>'],
        # '<ales>': ['<adj_list> ale', '<adj_list> ales', ],
        '<ales>': ['<stouts>', 'ale', 'ales'],
        '<stouts>': ['stout', 'stouts'],
        '<lager>': ['lager', 'lagers'],
        '<adj_list>': ['<adj> <adj_list>', '<adj>'],
        '<adj>': ['<color>', '<origin>', '<epsilon>'],
        '<color>': ['pale', 'brown'],
        '<origin>': ['india', 'american'],
        # '<sep>': ['-', ',', 'and'],
        '<epsilon>': [''],
    })

    terminal_symbols = ['', 'lager', 'lagers', 'ale', 'ales', 'stout', 'stouts', 'pale', 'brown', 'india', 'american'

    ]

    # @staticmethod
    # def build():
    #     rules = []
    #     for lh, rh in Grammar.grammar.items():
    #         # node = TreeNode(lh)
    #         # for r in rh:
    #         #     for s in r.split():
    #         #         sym_node = TreeNode(s)
    #         #         node.children.append(sym_node)
    #         # print_tree(node, '')
    #
    #         rules.append(ProductionRule(lh, rh))
        # setattr(Grammar, 'rules', rules)
        # cls.root_node = TreeNode()

    @staticmethod
    def beer_type_list(value):
        """
        An example of method to handle semantics. Name of method is significant so we can use getattr.
        :param value: Value to define a meaning to.
        :return:
        """
        print("semantics go here", value)


class DescriptionParser(object):
    """
    Builds the parse tree for a description.
    """
    description = ''

    def parse(self):

        stack = []
        remaining = self.tokens

        while len(remaining) > 0:
            self.shift(stack, remaining)
            while self.reduce(stack, len(remaining)):
                pass

        # while len(stack) > 1:
        # print(self.reduce(stack))

        # for i, e in enumerate(stack):
        #     new_stack = self.reduce([e])
        #     if new_stack:
        #         stack[i] = new_stack

        for e in stack:
            if isinstance(e, TreeNode):
                print_tree(e, '')
                print('\n')
        print(stack)

    def shift(self, stack, remaining):
        if len(remaining) > 0 and remaining[0] not in Grammar.terminal_symbols:
            # Remove any string not in our terminal symbols for now. We may do something with them later.
            remaining.remove(remaining[0])
            remaining.insert(0, '')  # add an epsilon

        stack.append(remaining[0])
        remaining.remove(remaining[0])

    def case_matches_stack(self, case, stack):

        for m in stack:
            if isinstance(m, str) and m in case:
                # If we have a string it is a terminal and if it is in the rule we have a match
                return case, 1
        # We make it here a tree is present in the stack. Map the strings to a list of strings to match a rule.
        # This could a combo of terminals and non terminals
        combo = list(map(lambda n: n.name if isinstance(n, TreeNode) else n, stack))
        return (case, len(combo)) if combo == case else (None, None)

    def reduce(self, stack, len_rem):
        for lh, rh in Grammar.grammar.items():
            for case in rh:
                case_as_list = [case]
                if lh != '<epsilon>':
                    case_as_list = case.split()
                is_match, match_length = self.case_matches_stack(case_as_list, stack[-len(case_as_list):])
                if is_match:
                    if (lh == '<type_list>' and len_rem is not 0) or (lh == '<beer>' and len(stack) is not 1):
                        # Don't reduce to type list or beer until all is parsed and stack is at one
                        continue
                    trees = list(map(lambda c: TreeNode(c) if isinstance(c, str) else c, stack[-match_length:]))
                    stack[-match_length:] = [TreeNode(lh, trees)]
                    # is_match = self.reduce(stack)
                    return stack
        return None

    def __init__(self, description):
        self.description = description
        self.tokens = list(map(lambda x: x.strip(string.punctuation), description.split()))

        # Create initial nodes

        # self.root_node = TreeNode(ProductionRule('beer', ['type_list']), 'beer')
        #

        # root_node = TreeNode('<beer>')
        #
        # stack = []
        # for token_index, token in enumerate(self.tokens):
        #     rule = getattr(Grammar, token, None)
        #     if rule:
        #
        #         # We found a terminal symbol
        #         t_node = TreeNode('"%s"' % token)  # Don't add to children until we have it's non terminal epsilon sibling
        #         # print(root_node.children)
        #         # Find index of terminal in rule
        #         # print(rule.left_hand)
        #         terminal_parent = TreeNode(rule.left_hand)
        #         for p_rule in Grammar.rules:
        #             for p in p_rule.non_terminals:
        #                 if rule.left_hand in p:
        #                     terminal_parent.children.append(TreeNode(p))
        #         stack.append(p)
        #         # parent.children.append(t_node)
        #         # root_node.children.append(terminal_parent)
        #
        #         # Find any non term nodes to the left of this term that would go to epsilon
        #         for i, term in enumerate(rule.terminals):
        #             if token in term:
        #                 rh_index = i
        #                 break
        #         if rule.non_terminals[rh_index]:
        #             for nt in rule.non_terminals[rh_index]:
        #                 if nt:
        #                     # We have found a non terminal
        #                     nt_node = TreeNode(nt)
        #                     nt_node.children.append(TreeNode('<epsilon>'))
        #                     terminal_parent.children.append(nt_node)
        #                     terminal_parent.children.append(t_node)
        #                     break
                # root_node.children.append(t_node)
        # print(root_node.children)

                # case = Grammar.grammar[rule.left_hand][rh_index]
                # print(case)
        # print_tree(root_node, '')


def print_tree(node, margin='--'):
    print('%s%s' % (margin, node.name))
    margin += '|--'
    # print(node.children[0].children)
    for child in node.children:
        print_tree(child, margin)
